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
                <div className='UserInfo'>
                    <span style={{marginTop: "1rem" }}> Welcome Back </span>
                    <span style={{marginTop: "1rem" }}> {auth.user?.profile.email} </span>
                    {/* <pre> ID Token: {auth.user?.id_token.slice(-20)} </pre>
                    <pre> Access Token: {auth.user?.access_token.slice(-20)} </pre>
                    <pre> Refresh Token: {auth.user?.refresh_token.slice(-20)} </pre> */}
                    <button onClick={handleLogout}>Log Out</button>

                    <p style={{ fontSize: "0.75rem", color: "#666" }}> 
                        Notice : No SES production access, alerts currently only work for email addresses verified by my SES account
                    </p>
                </div>

                <AlertCards models={models} userEmail={auth.user?.profile.email} userAlerts={userAlerts} setUserAlerts={setUserAlerts}/> 

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