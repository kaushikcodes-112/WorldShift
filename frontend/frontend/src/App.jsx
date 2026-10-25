import { useEffect, useState } from "react";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer
} from "recharts";

import { getCountries, getIndicators, compareCountries } from "./api";
import "./App.css";

function App() {
    const [countries, setCountries] = useState([]);
    const [indicators, setIndicators] = useState([]);

    const [country, setCountry] = useState("");
    const [peers, setPeers] = useState([]);
    const [indicator, setIndicator] = useState("");

    const [startYear, setStartYear] = useState(2000);
    const [endYear, setEndYear] = useState(2024);

    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadData() {
            try {
                const [countryData, indicatorData] = await Promise.all([
                    getCountries(),
                    getIndicators()
                ]);

                setCountries(countryData);
                setIndicators(indicatorData);
            } catch (err) {
                setError(`Could not load options: ${err.message}`);
            }
        }

        loadData();
    }, []);

    function handlePeerChange(event) {
        const selected = Array.from(
            event.target.selectedOptions,
            option => option.value
        );

        setPeers(selected.filter(code => code !== country));
    }

    async function handleCompare(event) {
        event.preventDefault();

        setError("");
        setResult(null);

        if (!country || !indicator || peers.length === 0) {
            setError("Select a main country, an indicator, and at least one peer.");
            return;
        }

        if (startYear >= endYear) {
            setError("The start year must be earlier than the end year.");
            return;
        }

        setLoading(true);

        try {
            const data = await compareCountries({
                country,
                peers,
                indicator,
                startYear,
                endYear
            });

            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    const countryNames = Object.fromEntries(
        countries.map(item => [item.code, item.name])
    );

    // Convert the backend's country-by-country histories
    // into rows that Recharts can plot by year.
    const chartData = [];

    if (result) {
        const histories = result.comparison.countries;

        const years = [
            ...new Set(
                Object.values(histories)
                    .flat()
                    .map(row => row.year)
            )
        ].sort((a, b) => a - b);

        for (const year of years) {
            const row = { year };

            for (const [code, observations] of Object.entries(histories)) {
                const observation = observations.find(
                    item => item.year === year
                );

                row[code] = observation?.value ?? null;
            }

            chartData.push(row);
        }
    }

    const selectedIndicator = indicators.find(
        item => item.id === indicator
    );

    const chartColors = [
        "#2563eb",
        "#dc2626",
        "#16a34a",
        "#9333ea",
        "#ea580c",
        "#0891b2",
        "#4f46e5"
    ];

    return (
        <main className="worldshift">
            <header className="page-header">
                <h1>WorldShift</h1>
                <p>
                    Explore development trends.
                    Compare countries. Investigate the gaps.
                </p>
            </header>

            <section className="panel">
                <h2>Build your comparison</h2>

                <form onSubmit={handleCompare}>
                    <label>
                        Main country

                        <select
                            value={country}
                            onChange={event => {
                                const selected = event.target.value;

                                setCountry(selected);
                                setPeers(previous =>
                                    previous.filter(code => code !== selected)
                                );
                            }}
                        >
                            <option value="">Select a country</option>

                            {countries.map(item => (
                                <option key={item.code} value={item.code}>
                                    {item.name}
                                </option>
                            ))}
                        </select>
                    </label>

                    <label>
                        Peer countries
                        <span className="hint">
                            Select multiple countries. Use Ctrl on Windows
                            or Cmd on Mac to select several.
                        </span>

                        <select
                            multiple
                            size={6}
                            value={peers}
                            onChange={handlePeerChange}
                        >
                            {countries
                                .filter(item => item.code !== country)
                                .map(item => (
                                    <option
                                        key={item.code}
                                        value={item.code}
                                    >
                                        {item.name}
                                    </option>
                                ))}
                        </select>
                    </label>

                    <label>
                        Indicator

                        <select
                            value={indicator}
                            onChange={event => setIndicator(event.target.value)}
                        >
                            <option value="">Select an indicator</option>

                            {indicators.map(item => (
                                <option key={item.id} value={item.id}>
                                    {item.name}
                                </option>
                            ))}
                        </select>
                    </label>

                    <div className="year-inputs">
                        <label>
                            Start year
                            <input
                                type="number"
                                value={startYear}
                                onChange={event =>
                                    setStartYear(Number(event.target.value))
                                }
                            />
                        </label>

                        <label>
                            End year
                            <input
                                type="number"
                                value={endYear}
                                onChange={event =>
                                    setEndYear(Number(event.target.value))
                                }
                            />
                        </label>
                    </div>

                    <button type="submit" disabled={loading}>
                        {loading ? "Comparing..." : "Compare countries"}
                    </button>
                </form>

                {error && <p className="error">{error}</p>}
            </section>

            {result && (
                <section className="panel results">
                    <h2>
                        {selectedIndicator?.name || indicator}
                    </h2>

                    <p>
                        {startYear}–{endYear}
                        {selectedIndicator?.unit
                            ? ` · ${selectedIndicator.unit}`
                            : ""}
                    </p>

                    {chartData.length > 0 ? (
                        <div className="chart-container">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart
                                    data={chartData}
                                    margin={{
                                        top: 10,
                                        right: 20,
                                        left: 20,
                                        bottom: 10
                                    }}
                                >
                                    <CartesianGrid strokeDasharray="3 3" />

                                    <XAxis
                                        dataKey="year"
                                        type="number"
                                        domain={["dataMin", "dataMax"]}
                                        tickFormatter={String}
                                    />

                                    <YAxis />

                                    <Tooltip
                                        labelFormatter={year => `Year: ${year}`}
                                    />

                                    <Legend />

                                    {Object.keys(
                                        result.comparison.countries
                                    ).map((code, index) => (
                                        <Line
                                            key={code}
                                            type="monotone"
                                            dataKey={code}
                                            name={countryNames[code] || code}
                                            stroke={
                                                chartColors[
                                                    index % chartColors.length
                                                ]
                                            }
                                            connectNulls={false}
                                            dot={false}
                                            activeDot={{ r: 5 }}
                                            strokeWidth={2}
                                        />
                                    ))}
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    ) : (
                        <p>No observations are available for this period.</p>
                    )}

                    <h3>Development gap by year</h3>

                    {result.gaps.length > 0 ? (
                        <div className="table-wrapper">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Year</th>
                                        <th>Main country</th>
                                        <th>Peer median</th>
                                        <th>Gap</th>
                                        <th>Relative gap</th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {result.gaps.map(gap => (
                                        <tr key={gap.year}>
                                            <td>{gap.year}</td>
                                            <td>{gap.main_value.toFixed(2)}</td>
                                            <td>{gap.peer_value.toFixed(2)}</td>
                                            <td>{gap.gap.toFixed(2)}</td>
                                            <td>
                                                {gap.relative_gap == null
                                                    ? "N/A"
                                                    : `${gap.relative_gap.toFixed(2)}%`}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    ) : (
                        <p>
                            No overlapping observations are available to
                            calculate development gaps.
                        </p>
                    )}

                    <h3>Progress comparison</h3>

                    {result.progress_analysis.status === "insufficient_data" ? (
                        <p>{result.progress_analysis.message}</p>
                    ) : (
                        <p>
                            Main country change:{" "}
                            {result.progress_analysis.main_change_pct.toFixed(2)}%
                            <br />
                            Peer median change:{" "}
                            {result.progress_analysis.peer_median_change_pct.toFixed(2)}%
                            <br />
                            Difference in percentage points:{" "}
                            {result.progress_analysis.difference_percentage_points.toFixed(2)}
                        </p>
                    )}
                </section>
            )}
        </main>
    );
}

export default App; 