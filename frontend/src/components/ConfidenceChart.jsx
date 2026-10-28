import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const COLORS = {
  NORMAL: '#2e9e44',
  PNEUMONIA: '#d64545',
}

function toPercent(value) {
  return `${(value * 100).toFixed(1)}%`
}

export default function ConfidenceChart({ probabilities }) {
  const data = probabilities.map((p) => ({
    name: p.name.toUpperCase(),
    value: p.prob,
  }))

  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 8 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis domain={[0, 1]} tickFormatter={toPercent} width={54} />
        <Tooltip formatter={toPercent} />
        <Bar dataKey="value" name="Xác suất" radius={[6, 6, 0, 0]}>
          {data.map((entry) => (
            <Cell key={entry.name} fill={COLORS[entry.name] || '#8884d8'} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
