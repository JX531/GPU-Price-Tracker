import '../App.css'

function Sidebar({modelList, selectedProduct, setSelectedProduct}) {
  return (
    <div className='Sidebar'>
      <h1>GPU Price Tracker</h1>
        <ul className='SidebarList'>
            {modelList.map(item =>
                <li key={item} className='row' id = {selectedProduct == item? "active" : ""} onClick={()=> setSelectedProduct(item)}>
                    <div>{item}</div>
                </li>
            )}
        </ul>
    </div>
  );
}

export default Sidebar;