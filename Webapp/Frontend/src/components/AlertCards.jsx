import '../App.css'
import { useState, useEffect } from 'react';
import putUserAlerts from '../apis/userAlerts/PUT'
import delUserAlerts from '../apis/userAlerts/DEL'

function AlertCards({models, userEmail, userAlerts, setUserAlerts}){
    const options = models.filter(model => !(userAlerts|| []).some(alert  => alert.Model == model))
    const [edittingModel, setEdittingModel] = useState("")
    const [edittingPrice, setEdittingPrice] = useState()
    const [deletingModel, setDeletingModel] = useState("")
    const [addingPrice, setAddingPrice] = useState()
    const [addingModel, setAddingModel] = useState(options[0] || "")

    const handleAdd = (model,price) =>{
        if (model == ""){
            return
        }
        
        putUserAlerts(userEmail, model, price)
        .then(() => {
            setUserAlerts(old => [...old,{"Model": model, "Price": price}])
            setAddingModel(options[0] || "")
        })
        .catch(error => console.log("Error handleAdd: ", error))
    }

    const handleEdit = (model, newPrice) => {
        putUserAlerts(userEmail, model, newPrice)
        .then(() => {
            setUserAlerts(old => old.map(item => item.Model == model ? {...item, "Price": newPrice} : item))
            setEdittingModel("")
        })
        .catch(error => console.log("Error handleEdit: ", error))
    }

    const handleDelete = (model) => {
        delUserAlerts(userEmail, model)
        .then(() => {
            setUserAlerts(old => old.filter(item => item.Model != model))
            setDeletingModel("")
        })
        .catch(error => console.log("Error handleDelete: ", error))
    }

    if (userAlerts.length == 0){
        return (
            <div>
                <div>No Alerts Set...</div>
        
                <div className='addAlertCard'>
                    <select onChange={(e) => setAddingModel(e.target.value)} defaultValue={""}>
                        <option value={""}>Select</option>
                        {options.map(model => (
                            <option value={model}>{model}</option>
                        ))}
                    </select>
                    <input type='number' value={addingPrice} onChange={e => setAddingPrice(Number(e.target.value))}/>
                    <button onClick={() => handleAdd(addingModel, addingPrice)}>Add</button>
                </div>
            </div>
        )
    }

    return (
        <div>
            {userAlerts.map(alert => {
                const editMode = alert.Model == edittingModel
                const deleteMode = alert.Model == deletingModel
                return(
                    <div>
                        <h2 style={{textDecoration: "underline", marginTop: "5rem"}}>Alerts Set</h2>
                        <div key={alert.Model} className='alertCard'>
                            <h3>{alert.Model}</h3>

                            {editMode ? 
                            (<input type='number' value={edittingPrice} onChange={e => setEdittingPrice(Number(e.target.value))}/>)
                            : 
                            (<p>${alert.Price}</p>)
                            }

                            {editMode ? 
                            (<div><button onClick={() => {edittingPrice != alert.Price ? handleEdit(alert.Model, edittingPrice) : setEdittingModel("")}}>Confirm Edit</button> <button onClick={() => {setEdittingModel("")}}>Cancel</button></div>)
                            : 
                            deleteMode ?
                            (<div><button onClick={() => {handleDelete(alert.Model)}}>Confirm Delete</button> <button onClick={() => {setDeletingModel("")}}>Cancel</button></div>)
                            :
                            (<div><button onClick={() => {setEdittingModel(alert.Model); setEdittingPrice(alert.Price)}}>Edit</button> <button onClick={() => {setDeletingModel(alert.Model)}}>Delete</button></div>)
                            }

                        </div>

                        <div className='addAlertCard'>
                            <select onChange={(e) => setAddingModel(e.target.value)} defaultValue={""}>
                                <option value={""}>Select</option>
                                {options.map(model => (
                                    <option value={model}>{model}</option>
                                ))}
                            </select>
                            <input type='number' value={addingPrice} onChange={e => setAddingPrice(Number(e.target.value))}/>
                            <button onClick={() => handleAdd(addingModel, addingPrice)}>Add</button>
                        </div>
                    </div>
                )
            })}
        </div>
    );
}

export default AlertCards