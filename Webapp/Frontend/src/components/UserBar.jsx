import '../App.css'
import signOutRedirect from '../hooks/UserRedirects'
import AlertCards from './AlertCards';
function UserBar({models, auth, userAlerts, setUserAlerts}){

    const handleLogout = async () =>{
        await auth.removeUser(); 
        signOutRedirect(); 
    }

    if (auth.isAuthenticated){
        return(
            <div className='UserBar'>
                <div>
                    <pre> Hello: {auth.user?.profile.email} </pre>
                    {/* <pre> ID Token: {auth.user?.id_token.slice(-20)} </pre>
                    <pre> Access Token: {auth.user?.access_token.slice(-20)} </pre>
                    <pre> Refresh Token: {auth.user?.refresh_token.slice(-20)} </pre> */}
                    <button onClick={handleLogout}>Log Out</button>
                    
                    <AlertCards models={models} userEmail={auth.user?.profile.email} userAlerts={userAlerts} setUserAlerts={setUserAlerts}/> 
                </div>
            </div>
        )
    }
    else return(
        <div className='UserBar'>
            <div>
                <button style={{ marginTop: "5rem"}} onClick={() => auth.signinRedirect()}>Log In / Register</button>
            </div>
        </div>
    )
}

export default UserBar