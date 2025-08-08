function signOutRedirect(){
    const clientId = "576eeff7apnq0rd2llscgfidov";
    const logoutUri = "https://d3pprnqmx0m8l1.cloudfront.net";
    const cognitoDomain = "https://ap-southeast-11wgwj1z1w.auth.ap-southeast-1.amazoncognito.com";
    window.location.href = `${cognitoDomain}/logout?client_id=${clientId}&logout_uri=${encodeURIComponent(logoutUri)}`;
  };

export default signOutRedirect