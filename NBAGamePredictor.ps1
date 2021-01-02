$TodaysDate = Get-Date -Format "yyyy/MM/dd"
$TodaysGames = (Invoke-RestMethod -UseBasicParsing -Uri "https://www.balldontlie.io/api/v1/games?dates[]=$TodaysDate").data | Select-Object home_team,visitor_team

foreach ($Game in $TodaysGames) {
    $HomeTeam = New-Object -TypeName "System.Collections.ArrayList"
    $AwayTeam = New-Object -TypeName "System.Collections.ArrayList"
    
    [pscustomobject]@{
        HomeTeam = $Game.home_team.full_name
        AwayTean = $Game.visitor_team.full_name
    }
}
