import '../App.css'

function DataTable({data}){
    if (!Array.isArray(data)) {
      return <div>Loading table...</div>
    }
      return (
    <table className="DataTable">
      <thead>
        <tr>
          <th>No.</th>
          <th>Date</th>
          <th>Average Price</th>
          <th>No. Listings</th>
        </tr>
      </thead>
      <tbody>
        {data.map((d, i) => (
          <tr key={i}>
            <td>{i+1}</td>
            <td>{d.Date}</td>
            <td>{d.AvgPrice}</td>
            <td>{d.NumListings}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default DataTable;