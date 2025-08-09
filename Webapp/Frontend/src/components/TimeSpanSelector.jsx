import '../App.css'

function TimeSpanSelector({timeSpan, setTimeSpan}){
    return(
        <select defaultValue={-365} className='select' onChange={(e) => setTimeSpan(e.target.value)}>
          <option value={-7}>Past 7 Days</option>
          <option value={-30}>Past 30 Days</option>
          <option value={-90}>Past 90 Days</option>
          <option value={-365}>Past 365 Days</option>
        </select>
    )
}

export default TimeSpanSelector