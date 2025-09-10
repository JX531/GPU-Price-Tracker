import '../App.css'
import { useState, useEffect } from 'react';
import putUserAlerts from '../apis/userAlerts/PUT'
import delUserAlerts from '../apis/userAlerts/DEL'
import updateCachedAlerts from '../helpers/updateCachedAlerts';

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
            setUserAlerts(old => {
                const updatedAlerts = [...old,{"Model": model, "Price": price}]
                updateCachedAlerts(updatedAlerts,userEmail)
                return updatedAlerts
            })
            setAddingModel("")
        })
        .catch(error => console.log("Error handleAdd: ", error))
    }

    const handleEdit = (model, newPrice) => {
        putUserAlerts(userEmail, model, newPrice)
        .then(() => {
            setUserAlerts(old => {
                const updatedAlerts = old.map(item => item.Model == model ? {...item, "Price": newPrice} : item)
                updateCachedAlerts(updateCachedAlerts,userEmail)
                return updatedAlerts
            })
            setEdittingModel("")
        })
        .catch(error => console.log("Error handleEdit: ", error))
    }

    const handleDelete = (model) => {
        delUserAlerts(userEmail, model)
        .then(() => {
            setUserAlerts(old => {
                const updatedAlerts = old.filter(item => item.Model != model)
                updateCachedAlerts(updatedAlerts, userEmail)
                return updatedAlerts
            })
            setDeletingModel("")
        })
        .catch(error => console.log("Error handleDelete: ", error))
    }


    return (
        <div>
            <div>
                <span style={{textDecoration: "underline", marginTop: "1rem"}}>Alerts Set</span>          
                <div className='AddAlertCard'>
                    <select onChange={(e) => {setAddingModel(e.target.value)}} value={addingModel}>
                        <option value={""}>Select</option>
                        {options.map(model => (
                            <option value={model}>{model}</option>
                        ))}
                    </select>
                    <input type='number' value={addingPrice} onChange={e => setAddingPrice(Number(e.target.value))}/>
                    <button onClick={() => handleAdd(addingModel, addingPrice)}>Add</button>
                </div>

            </div>

            <div className='AlertCardContainer'>

                {userAlerts.length == 0 ? //Is the userAlerts array empty?
                (<div style={{marginTop: "1rem"}}>No Alerts Set...</div>) //No models to show, just show a "No Alerts Set" text
                : 
                userAlerts.map(alert => {//Theres alerts, so map them and show a card for each

                    //Setting Edit Mode or Delete Mode for the current model
                    //Done by checking if edittingModel or deletingModel is set to current model
                    const editMode = alert.Model == edittingModel
                    const deleteMode = alert.Model == deletingModel

                    return(
                        <div>
                            <div key={alert.Model} className='AlertCard'>
                                <h3>{alert.Model}</h3>

                                {/* PRICE DISPLAY */}
                                {editMode ? //Is editMode enabled for current Model?

                                //In Editting Mode, transform the price display into an input box
                                (<input type='number' value={edittingPrice} onChange={e => setEdittingPrice(Number(e.target.value))}/>) 
                                : 
                                //Not in Editting Mode, just display the price
                                (<p>${alert.Price}</p>) 
                                }
                                
                                {/* BUTTONS BELOW PRICE */}
                                {editMode ? //Is editMode enabled for current Model?

                                //In Editting Mode, the buttons become "Confirm Edit" and "Cancel". "Confirm Edit" checks if new price != old price, then calls handleEdit, otherwise it just resets edittingModel. Cancel just resets edittingModel.
                                (<div><button onClick={() => {edittingPrice != alert.Price ? handleEdit(alert.Model, edittingPrice) : setEdittingModel("")}}>Confirm Edit</button> <button onClick={() => {setEdittingModel("")}}>Cancel</button></div>)
                                : 
                                //Not in Editting Mode, check if in Delete Mode
                                deleteMode ? //Is deleteMode enabled for current Model?

                                //In Delete Mode, the buttons become "Confirm Delete" and "Cancel". "Confirm Delete" calls handleDelete, "Cancel" just resets deletingModel.
                                (<div><button onClick={() => {handleDelete(alert.Model)}}>Confirm Delete</button> <button onClick={() => {setDeletingModel("")}}>Cancel</button></div>)
                                :
                                //Not in Edit Mode and not in Delete Mode, this is the default button display with "Edit" and "Delete" options. Each button will enable their respective mode for the current model.
                                (<div><button onClick={() => {setEdittingModel(alert.Model); setEdittingPrice(alert.Price)}}>Edit</button> <button onClick={() => {setDeletingModel(alert.Model)}}>Delete</button></div>)
                                }

                            </div>
                        </div>
                    )
                })}

            </div>
        </div>
    );
}

export default AlertCards