import pandas as pd

def calculate_wellness_score(sleep, water, mood, energy):
    score = 0
    # Sleep (max 25 points, optimal 8 hours)
    score += min((sleep / 8.0) * 25, 25) if sleep else 0
    
    # Water (max 25 points, optimal 8 glasses)
    score += min((water / 8.0) * 25, 25) if water else 0
    
    # Mood (max 25 points)
    mood_scores = {
        "😊 Happy": 25, "😌 Calm": 25, "🤩 Energetic": 25,
        "😴 Tired": 15, "😔 Sad": 15, "😡 Irritated": 15,
        "😣 Stressed": 10, "😰 Anxious": 10
    }
    score += mood_scores.get(mood, 15) if mood else 15
    
    # Energy (max 25 points, scale 1-10)
    score += (energy / 10.0) * 25 if energy else 0
    
    return int(min(score, 100))

def get_wellness_category(score):
    if score >= 80:
        return "🌸 Excellent"
    elif score >= 60:
        return "🌷 Good"
    elif score >= 40:
        return "🌼 Moderate"
    else:
        return "🍂 Needs Attention"

def generate_simple_insights(df):
    insights = []
    if df.empty or len(df) < 2:
        return ["Not enough data yet. Keep logging to see insights!"]
        
    # Energy trend
    recent_energy = df['energy'].iloc[-1]
    prev_energy = df['energy'].iloc[-2]
    if recent_energy > prev_energy:
        insights.append("⚡ Your energy is improving compared to your last log.")
    elif recent_energy < prev_energy:
        insights.append("🔋 Your energy has dropped slightly.")
        
    # Stress trend
    recent_stress = df['stress'].iloc[-1]
    prev_stress = df['stress'].iloc[-2]
    if recent_stress > prev_stress:
        insights.append("😌 Stress levels have increased recently. Take some time to relax.")
    elif recent_stress < prev_stress:
        insights.append("✨ Great job keeping your stress levels down!")
    
    # Sleep trend
    recent_sleep = df['sleep'].iloc[-1]
    prev_sleep = df['sleep'].iloc[-2]
    if recent_sleep > prev_sleep:
        insights.append("🌙 Sleep improved compared to your last log.")
    elif recent_sleep < 6:
        insights.append("😴 You might need more rest. Try to aim for 8 hours.")
        
    if not insights:
        insights.append("🌟 You're maintaining a steady wellness routine!")
        
    return insights
