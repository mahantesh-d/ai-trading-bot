import { useEffect, useState } from "react";

export default function TradingDashboard() {

  const [status, setStatus] = useState({});
  const [trades, setTrades] = useState([]);

  useEffect(() => {

const fetchData = async () => {

try {

  // Status API
  const statusRes = await fetch(
    "http://127.0.0.1:8000/status"
  )

  const statusData = await statusRes.json()

  setStatus(statusData)

  // Trades API
  const tradesRes = await fetch(
    "http://127.0.0.1:8000/trades"
  )

  const tradesData = await tradesRes.json()

  setTrades(tradesData)

} catch (error) {

  console.error(
    "Fetch error:",
    error
  )
}

}

// Initial fetch
fetchData()

// Auto refresh every 5 seconds
const interval = setInterval(
fetchData,
5000
)

// Cleanup
return () => clearInterval(interval)

}, [])

  return (

    <div className="min-h-screen bg-gray-100 p-6">

      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div>

          <h1 className="text-4xl font-bold">
            AI Trading Bot Dashboard
          </h1>

          <p className="text-gray-600 mt-2">
            Monitor signals, trades, and bot performance.
          </p>

        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

          <div className="bg-white rounded-2xl shadow-sm p-6">
            <p className="text-sm text-gray-500">
              Bot Status
            </p>

            <h2 className="text-2xl font-semibold mt-2">
              {status.bot_status}
            </h2>
          </div>

          <div className="bg-white rounded-2xl shadow-sm p-6">
            <p className="text-sm text-gray-500">
              Current Signal
            </p>

            <h2 className="text-2xl font-semibold mt-2">
              {status.signal}
            </h2>
          </div>

          <div className="bg-white rounded-2xl shadow-sm p-6">
            <p className="text-sm text-gray-500">
              Open Position
            </p>

            <h2 className="text-2xl font-semibold mt-2">
              {status.position}
            </h2>
          </div>

          <div className="bg-white rounded-2xl shadow-sm p-6">
            <p className="text-sm text-gray-500">
              Daily PnL
            </p>

            <h2 className="text-2xl font-semibold mt-2">
              ₹{status.daily_pnl}
            </h2>
          </div>

        </div>

        {/* Trades */}
        <div className="bg-white rounded-2xl shadow-sm p-6">

          <div className="flex items-center justify-between mb-4">

            <h2 className="text-xl font-semibold">
              Recent Trades
            </h2>

          </div>

          <div className="overflow-x-auto">

            <table className="w-full text-left">

              <thead>

                <tr className="border-b">

                  <th className="py-3">
                    Time
                  </th>

                  <th className="py-3">
                    Signal
                  </th>

                  <th className="py-3">
                    Instrument
                  </th>

                  <th className="py-3">
                    Entry
                  </th>

                  <th className="py-3">
                    PnL
                  </th>

                </tr>

              </thead>

              <tbody>

                {trades.map((trade, index) => (

                  <tr
                    key={index}
                    className="border-b last:border-none"
                  >

                    <td className="py-4">
                      {trade.time}
                    </td>

                    <td className="py-4">
                      {trade.signal}
                    </td>

                    <td className="py-4">
                      {trade.instrument}
                    </td>

                    <td className="py-4">
                      ₹{trade.entry}
                    </td>

                    <td className="py-4">
                      {trade.pnl}
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        </div>

      </div>

    </div>

  );
}