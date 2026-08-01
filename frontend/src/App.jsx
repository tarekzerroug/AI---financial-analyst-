import { useMemo, useState } from "react";

const API_BASE = (import.meta.env.VITE_API_URL || "/api").replace(/\/$/, "");
const TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "JPM"];

function money(value) {
  const number = Number(value);
  return Number.isFinite(number) ? `$${number.toFixed(2)}` : "-";
}

function dateOnly(value) {
  return value ? String(value).slice(0, 10) : "";
}

function parseDate(value) {
  return new Date(`${dateOnly(value)}T00:00:00`).getTime();
}

async function fetchJson(path, options) {
  const response = await fetch(`${API_BASE}${path}`, options);
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

function closestRow(rows, selectedDate) {
  if (!rows.length) return null;
  if (!selectedDate) return rows.at(-1);

  const target = parseDate(selectedDate);
  return rows.reduce((closest, row) => {
    const distance = Math.abs(parseDate(row.date) - target);
    const closestDistance = Math.abs(parseDate(closest.date) - target);
    return distance < closestDistance ? row : closest;
  }, rows[0]);
}

function compactNews(article) {
  return {
    title: article.title || "Untitled",
    url: article.url,
    source: article.source,
    summary: article.summary,
    published_at: article.time_published || article.published_at,
    sentiment: article.overall_sentiment_label,
    score: article.overall_sentiment_score
  };
}

function makePrompt({ ticker, priceRow, news }) {
  const latestNews = news.length
    ? news.map((item, index) => `${index + 1}. ${item.title} (${item.sentiment || "n/a"}): ${item.summary || item.url || ""}`).join("\n")
    : "No latest news returned by the news API.";

  return `You are an AI financial analyst. Create a structured report for ${ticker}.

Price data from PostgreSQL:
- Date: ${dateOnly(priceRow.date)}
- Open price: ${money(priceRow.open)}
- Close price: ${money(priceRow.close)}
- Volume: ${priceRow.volume ?? "n/a"}

Latest news:
${latestNews}

Return a concise report with: summary, price move, sentiment, catalysts, risks, and a confidence level.`;
}

export default function App() {
  const [ticker, setTicker] = useState("AAPL");
  const [selectedDate, setSelectedDate] = useState("");
  const [prices, setPrices] = useState([]);
  const [news, setNews] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [report, setReport] = useState("");
  const [status, setStatus] = useState("Ready");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const sortedPrices = useMemo(
    () => [...prices].sort((a, b) => parseDate(a.date) - parseDate(b.date)),
    [prices]
  );

  const priceRow = closestRow(sortedPrices, selectedDate);
  const move = priceRow ? ((Number(priceRow.close) - Number(priceRow.open)) / Number(priceRow.open)) * 100 : null;

  async function generateReport(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setReport("");
    setStatus("Loading market data");

    try {
      const cleanTicker = ticker.trim().toUpperCase();
      const [priceRows, newsRows] = await Promise.all([
        fetchJson(`/prices/${cleanTicker}`),
        fetchJson(`/news/${cleanTicker}`).catch(() => [])
      ]);

      const orderedPrices = [...priceRows].sort((a, b) => parseDate(a.date) - parseDate(b.date));
      const latest = orderedPrices.at(-1);
      const nextDate = selectedDate || dateOnly(latest?.date);
      const nextPriceRow = closestRow(orderedPrices, nextDate);
      const nextNews = newsRows.slice(0, 6).map(compactNews);
      const nextPrompt = makePrompt({
        ticker: cleanTicker,
        priceRow: nextPriceRow,
        news: nextNews
      });

      setTicker(cleanTicker);
      setPrices(orderedPrices);
      setNews(nextNews);
      setSelectedDate(nextDate);
      setPrompt(nextPrompt);
      setStatus("Sending analysis request");

      const analysis = await fetchJson("/analysis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker: cleanTicker,
          date: dateOnly(nextPriceRow.date),
          selected_date: nextDate,
          open_price: Number(nextPriceRow.open),
          close_price: Number(nextPriceRow.close),
          volume: Number(nextPriceRow.volume),
          latest_news: nextNews,
          prompt: nextPrompt
        })
      }).catch(() => null);

      setReport(analysis?.report || analysis?.analysis || analysis?.content || "");
      setStatus(analysis ? "Report generated" : "Prompt ready");
    } catch (err) {
      setError("Could not load data for this ticker. Check the backend, database, and news API key.");
      setStatus("Error");
    } finally {
      setLoading(false);
    }
  }

  async function copyPrompt() {
    if (!prompt) return;
    await navigator.clipboard.writeText(prompt);
    setStatus("Prompt copied");
  }

  return (
    <main className="app">
      <header className="topbar">
        <div>
          <p className="eyebrow">AI Financial Analytics Platform</p>
          <h1>Financial analyst workspace</h1>
        </div>
        <span className="status">{status}</span>
      </header>

      <div className="workspace">
        <form className="controls" onSubmit={generateReport}>
          <label>
            Ticker
            <input list="tickers" value={ticker} onChange={(event) => setTicker(event.target.value)} placeholder="AAPL" />
            <datalist id="tickers">
              {TICKERS.map((item) => <option key={item} value={item} />)}
            </datalist>
          </label>

          <label>
            Date
            <input type="date" value={selectedDate} onChange={(event) => setSelectedDate(event.target.value)} />
          </label>

          <button disabled={loading}>{loading ? "Generating..." : "Generate report"}</button>
          {error && <p className="error">{error}</p>}
        </form>

        <section className="results">
          <section className="metrics">
            <div>
              <span>Open</span>
              <strong>{priceRow ? money(priceRow.open) : "-"}</strong>
              <small>{priceRow ? dateOnly(priceRow.date) : "No date"}</small>
            </div>
            <div>
              <span>Close</span>
              <strong>{priceRow ? money(priceRow.close) : "-"}</strong>
              <small>{priceRow ? dateOnly(priceRow.date) : "No date"}</small>
            </div>
            <div>
              <span>Move</span>
              <strong className={move >= 0 ? "positive" : "negative"}>{move === null ? "-" : `${move.toFixed(2)}%`}</strong>
              <small>{prices.length ? `${prices.length} rows` : "No prices loaded"}</small>
            </div>
          </section>

          <section className="output">
            <div className="section-title">
              <h2>{report ? "LLM report" : "LLM prompt"}</h2>
              <button type="button" className="ghost" onClick={copyPrompt} disabled={!prompt}>Copy</button>
            </div>
            <pre>{report || prompt || "Choose a ticker and dates, then generate a report."}</pre>
          </section>

          <section className="news">
            <h2>Latest news</h2>
            {news.length ? news.map((item) => (
              <article key={`${item.title}-${item.published_at}`}>
                <a href={item.url} target="_blank" rel="noreferrer">{item.title}</a>
                <span>{item.sentiment || item.source || "Market news"}</span>
              </article>
            )) : <p>No news loaded.</p>}
          </section>
        </section>
      </div>
    </main>
  );
}
