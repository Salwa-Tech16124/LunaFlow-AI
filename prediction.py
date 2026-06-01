from datetime import timedelta, date

def calculate_predictions(last_period_start, cycle_length):
    """Calculate future cycle predictions based on past data."""
    next_period_date = last_period_start + timedelta(days=cycle_length)
    
    # Ovulation is estimated typically 14 days before the next period
    ovulation_date = next_period_date - timedelta(days=14)
    
    # Fertile window is typically 5 days before ovulation to 1 day after
    fertile_start = ovulation_date - timedelta(days=5)
    fertile_end = ovulation_date + timedelta(days=1)
    
    return {
        "next_period_date": next_period_date,
        "ovulation_date": ovulation_date,
        "fertile_window_start": fertile_start,
        "fertile_window_end": fertile_end
    }

def get_current_cycle_day(last_period_start, current_date=None):
    """Calculate the current cycle day."""
    if current_date is None:
        current_date = date.today()
    delta = current_date - last_period_start
    # Cycle day 1 is the first day of the period
    return delta.days + 1

def get_cycle_phase(last_period_start, cycle_length, period_duration):
    today = date.today()
    current_day = get_current_cycle_day(last_period_start)
    
    preds = calculate_predictions(last_period_start, cycle_length)
    ovulation_day = (preds['ovulation_date'] - last_period_start).days + 1
    
    if current_day <= period_duration:
        return "🩸 Menstrual Phase", "Your body is shedding its lining. Rest and hydrate."
    elif current_day < ovulation_day - 2:
        return "🌱 Follicular Phase", "Energy is rising. Great time for new projects and exercise!"
    elif current_day >= ovulation_day - 2 and current_day <= ovulation_day + 1:
        return "🌕 Ovulation Phase", "Peak energy and fertility. Stay hydrated and maintain balanced nutrition."
    else:
        return "🍂 Luteal Phase", "Winding down. You might experience PMS. Reduce caffeine and prioritize sleep."
