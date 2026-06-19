/**
 * Main Dashboard page - orchestrates Frontbook and Backbook sections
 * MVP: Placeholder, will be filled in Phase 3
 */
function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          NORAM Business Dashboard
        </h1>

        <div className="grid grid-cols-1 gap-8">
          {/* Placeholder for Frontbook section */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Frontbook Analytics
            </h2>
            <p className="text-gray-600">Dashboard coming soon...</p>
          </div>

          {/* Placeholder for Backbook section */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Backbook Analytics
            </h2>
            <p className="text-gray-600">Dashboard coming soon...</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
