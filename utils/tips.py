import random

def generate_wellness_tip(phase_name, mood=None, energy=None):
    if energy and int(energy) < 4:
        return "Your energy is low today. Try taking a short nap, stretching, and eating iron-rich foods."
        
    if mood in ["😔 Sad", "😰 Anxious", "😣 Stressed", "😡 Irritated"]:
        return "Try deep breathing exercises, short breaks, or listening to calming music to lift your mood."
        
    if "Menstrual" in phase_name:
        tips = [
            "Eat iron-rich foods and stay hydrated.",
            "Rest your body and try gentle yoga if you have cramps.",
            "Use a heating pad to soothe abdominal discomfort."
        ]
        return random.choice(tips)
    elif "Follicular" in phase_name:
        tips = [
            "Your energy is rising! This is a great time to start new projects.",
            "Try incorporating more fresh vegetables and light proteins.",
            "Perfect time for cardiovascular exercises and outdoor runs."
        ]
        return random.choice(tips)
    elif "Ovulation" in phase_name:
        tips = [
            "Great time for physical activity and outdoor walks.",
            "Your fertility is at its peak! Focus on balanced nutrition.",
            "You might feel more social and energetic. Enjoy connecting with others."
        ]
        return random.choice(tips)
    elif "Luteal" in phase_name:
        tips = [
            "Reduce caffeine and prioritize sleep.",
            "You might experience PMS symptoms. Be gentle with yourself.",
            "Focus on complex carbohydrates to maintain stable blood sugar levels."
        ]
        return random.choice(tips)
        
    return "Remember to drink 8 glasses of water and get plenty of rest!"
