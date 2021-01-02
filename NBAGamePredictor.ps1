$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("if-none-match", "`"802af375f65c2e0e9b80df0a448dadfe`"")
$TodaysGames = (Invoke-RestMethod 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json' -Method 'GET' -Headers $headers).scoreboard.games

$BasketBallDataPoints = foreach ($Game in $TodaysGames) {
    [pscustomobject]@{
        'Home Team' = $Game.hometeam.teamname
        'HomeWins' = $Game.hometeam.wins 
        'HomeLosses' = $Game.hometeam.losses
        'Away Team' = $Game.awayteam.teamname
        'AwayWins' = $Game.awayteam.wins
        'AwayLosses' = $Game.awayteam.losses
    }
}

$BasketBallDataPoints | Sort-Object HomeWins -Descending | Format-Table 
