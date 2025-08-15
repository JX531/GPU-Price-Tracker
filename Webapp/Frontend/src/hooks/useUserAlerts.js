import { useState, useEffect } from 'react';
import getUserAlerts from '../apis/userAlerts/GET';

function useUserAlerts(userEmail){
    const [userAlerts, setUserAlerts] = useState([])

    useEffect(()=>{

        if (!userEmail){
            console.log("useUserAlerts missing userEmail")
            return 
        }

        //if logged in, get their alerts
        if (userEmail){
            getUserAlerts(userEmail)
            .then(res => setUserAlerts(res || []))
            .catch(error => console.log("useUserAlerts failed, error: ", error))
        }
        
        //else if logged out, clear
        else setUserAlerts([])

    }, [userEmail])

    return {userAlerts, setUserAlerts}
}

export default useUserAlerts