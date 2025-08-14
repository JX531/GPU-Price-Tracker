import './App.css'

//Components
import Sidebar from './components/Sidebar'
import UserBar from './components/UserBar'
import DataTable from './components/DataTable'
import LineGraph from './components/LineGraph'
import TimeSpanSelector from './components/TimeSpanSelector'

import CheapestListingCards from './components/CheapestListingCards'

//Hooks
import useModels from './hooks/useModels'
import useModelData from './hooks/useModelData'
import useModelCheapest from './hooks/useModelCheapest'
import usePresentingData from './hooks/usePresentingData'


//Auth
import { useAuth } from "react-oidc-context";

function App() {

  //Auth
  const auth = useAuth();

  if (auth.isLoading) {
    return <div>Loading...</div>;
  }

  if (auth.error) {
    return <div>Encountering error... {auth.error.message}</div>;
  }
  //

  const {models, selectedProduct, setSelectedProduct} = useModels()
  const {selectedProductData} = useModelData(selectedProduct)
  const {selectedProductCheapest} = useModelCheapest(selectedProduct)
  const {presentingData, timeSpan, setTimeSpan} = usePresentingData(selectedProductData)

  return (
    <div className='App'>
      <Sidebar modelList={models} selectedProduct={selectedProduct} setSelectedProduct={setSelectedProduct}/>
      <div className="Content">

        <div className="DataContainer">
          <div>
            <TimeSpanSelector timeSpan={timeSpan} setTimeSpan={setTimeSpan}/>
          </div>
          
          <div className="ChartContainer">
            <LineGraph data={presentingData} />
          </div>

          <div className='TableContainer'>
            <DataTable data={presentingData} />
          </div>
        </div>

        <div className="CardContainer">
            <CheapestListingCards selectedProductCheapest={selectedProductCheapest} />
        </div>

      </div>
      <UserBar auth={auth}/>
    </div>
  )
}

export default App
