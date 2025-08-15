function updateCachedAlerts(userAlerts, userEmail){
    localStorage.setItem('userAlerts', JSON.stringify({"Data": userAlerts, "TimeStamp": Date.now(), "Email": userEmail}))
    console.log("Updated local cache")
}

export default updateCachedAlerts
