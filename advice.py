from sound_object import Sound

def compare_sound_properties(reference, learner, tolerance=0.15):
    def compare_individual(prop_name):
        ref_value = getattr(reference, prop_name)
        learner_value = getattr(learner, prop_name)

        target_range = (1 - tolerance) * ref_value, (1 + tolerance) * ref_value

        if target_range[0] <= learner_value <= target_range[1]:
            return 'close to the target'
        elif learner_value < target_range[0]:
            return 'too low'
        else:
            return 'too high'

    results = {}
    properties = ['average_f1', 'average_f2', 'difference_f1_f2']

    for prop in properties:
        results[prop] = compare_individual(prop)

    return results


def adjust_mouth_position(reference, learner):

    advice = compare_sound_properties(reference, learner)
    f1_adjustment = ""
    f2_adjustment = ""

    for prop, result in advice.items():
        if 'average_f1' in prop:
            if result == 'too low':
                f1_adjustment += f"Your F1 is {result}. Open your mouth more and/or lower your tongue position to increase F1.\n"
            elif result == 'too high':
                f1_adjustment += f"Your F1 is {result}. Close your mouth slightly and/or raise your tongue position to decrease F1.\n"
            else:
                f1_adjustment += f"Your F1 is {result}. Maintain the current mouth and tongue position for F1.\n"
        elif 'average_f2' in prop:
            if result == 'too low':
                f2_adjustment += f"Your F2 is {result}. Position the tongue closer to the front of the mouth to increase F2.\n"
            elif result == 'too high':
                f2_adjustment += f"Your F2 is {result}. Move the tongue towards the back of the mouth to decrease F2. \n"
            else:
                f2_adjustment += f"Your F2 is {result}. Maintain the current tongue position for F2.\n"

    return f1_adjustment + '\n' + f2_adjustment




def calculate_average_formant(formant_list): #[(t, formant), ...]
    if not formant_list:
        return None  # Handle the case where the list is empty

        # Extract the y values from the tuples
    y_values = [y for _, y in data]

    # Calculate the average of the y values
    average_y = sum(y_values) / len(y_values)

    return average_y