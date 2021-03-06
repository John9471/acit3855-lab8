import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://acit3855.eastus2.cloudapp.azure.com:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                // console.log(result.text());
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Items in inventory</th>
							<th>Number of Orders</th>
						</tr>
						<tr>
							<td># Items: {stats["items"]}</td>
							<td># Orders: {stats['orders']}</td>
						</tr>
						<tr>
							<td colSpan="2">Last Item: {stats["lastitem"]["name"]}</td>
						</tr>
						<tr>
							<td colSpan="2">Last Order: {stats['lastorder']["drink"]}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['lastupdated']}</h3>

            </div>
        )
    }
}
