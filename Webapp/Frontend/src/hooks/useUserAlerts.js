import { useState, useEffect } from 'react';
import getUserAlerts from '../apis/userAlerts/GET';
import tryCachedAlerts from '../helpers/tryCachedAlerts';

function useUserAlerts(userEmail){
    const [userAlerts, setUserAlerts] = useState(tryCachedAlerts(userEmail) || [])

    useEffect(()=>{

        if (!userEmail){
            console.log("useUserAlerts missing userEmail")
            return 
        }

        //if logged in, get their alerts
        getUserAlerts(userEmail)
        .then(res => setUserAlerts(res || []))
        .catch(error => console.log("useUserAlerts failed, error: ", error))
        

    }, [userEmail])

    return {userAlerts, setUserAlerts}
}

export default useUserAlerts