import pandas as pd

def parse_match(match_dict):
    """
    Parse Cricsheet match dictionary into delivery-level DataFrame.
    """
    deliveries = []
    innings = match_dict.get('innings', [])

    for inning in innings:
        for inning_name, inning_data in inning.items():
            batting_team = inning_data.get('team', 'Unknown')
            for delivery in inning_data.get('deliveries', []):
                for ball_number, ball_info in delivery.items():
                    row = {
                        'inning': inning_name,
                        'batting_team': batting_team,
                        'ball': ball_number,
                        'batsman': ball_info.get('batsman'),
                        'bowler': ball_info.get('bowler'),
                        'runs_total': ball_info.get('runs', {}).get('total', 0),
                        'runs_batter': ball_info.get('runs', {}).get('batsman', 0),
                        'runs_extras': ball_info.get('runs', {}).get('extras', 0),
                        'extras_type': list(ball_info.get('extras', {}).keys())[0] if ball_info.get('extras') else None,
                        'dismissal': ball_info.get('wicket', {}).get('kind'),
                        'fielder': (
                            ', '.join(ball_info['wicket'].get('fielders', []))
                            if 'fielders' in ball_info.get('wicket', {})
                            else ball_info.get('wicket', {}).get('fielder')
                        )
                    }
                    deliveries.append(row)

    return pd.DataFrame(deliveries)
