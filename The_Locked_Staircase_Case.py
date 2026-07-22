# Project: The Locked Staircase Case
# Description: An interactive text-based adventure game.
# The player controls Mo, a high school student who investigates a hidden
# laboratory area with his classmate T.


def write_log(log_file, message):
    """Write one message to the investigation log file."""
    try:
        with open(log_file, "a", encoding="utf-8") as file:
            file.write(message + "\n")
    except OSError:
        print("Warning: The investigation log could not be updated.")


def create_new_log_file():
    """Create and return a new log file name for one playthrough."""
    number = 1

    while True:
        if number == 1:
            log_file = "Investigation_Log.txt"
        else:
            log_file = "Investigation_Log_" + str(number) + ".txt"

        try:
            with open(log_file, "x", encoding="utf-8") as file:
                file.write("")
            return log_file
        except FileExistsError:
            number = number + 1
        except OSError:
            print("Warning: A new investigation log could not be created.")
            return "Investigation_Log.txt"


def story_time(state):
    """Return the current in-game time as a string."""
    minutes_passed = 130 - state["minutes_left"]
    if minutes_passed < 0:
        minutes_passed = 0

    total_minutes = 12 * 60 + minutes_passed
    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours < 10:
        hours_text = "0" + str(hours)
    else:
        hours_text = str(hours)

    if minutes < 10:
        minutes_text = "0" + str(minutes)
    else:
        minutes_text = str(minutes)

    return hours_text + ":" + minutes_text


def write_timed_log(log_file, state, message):
    """Write a log message with the current story time."""
    write_log(log_file, "[" + story_time(state) + "] " + message)


def start_log(log_file):
    """Start a new log file for this playthrough."""
    write_log(log_file, "=" * 60)
    write_log(log_file, "  NEW INVESTIGATION STARTED")
    write_log(log_file, "=" * 60)
    write_log(log_file, "[12:00] Mo started a new investigation after the morning classes ended.")


def create_initial_state():
    """Create and return the starting game state."""
    return {
        "stage": 1,
        "minutes_left": 130,
        "evidence": [],
        "noise": 0,
        "phone_used": False,
        "game_over": False,
        "ending": "",
        "pending_output": ""
    }


def time_string(minutes_left):
    """Convert minutes into a readable time string."""
    if minutes_left < 0:
        minutes_left = 0

    hours = minutes_left // 60
    minutes = minutes_left % 60

    if hours == 0:
        return str(minutes) + " minutes"
    if minutes == 0:
        return str(hours) + " hour(s)"
    return str(hours) + " hour(s) and " + str(minutes) + " minutes"


def add_evidence(state, item, log_file):
    """Add useful evidence to the evidence list if it is not already there."""
    if item not in state["evidence"]:
        state["evidence"].append(item)
        write_timed_log(log_file, state, "Evidence collected: " + item)
    return state


def spend_time(state, minutes, action, log_file):
    """Reduce time and record the action in the investigation log."""
    state["minutes_left"] = state["minutes_left"] - minutes
    write_timed_log(log_file, state, action + " | Time spent: " + str(minutes) + " minutes")

    if state["minutes_left"] <= 0 and not state["game_over"]:
        state["game_over"] = True
        state["ending"] = "time_failure"
        write_timed_log(log_file, state, "The player ran out of time.")

    return state


def check_noise(state, log_file):
    """End the game if the player has made too much noise."""
    if state["noise"] >= 3 and not state["game_over"]:
        state["game_over"] = True
        state["ending"] = "caught_failure"
        write_timed_log(log_file, state, "The player made too much noise and was discovered.")
    return state


def get_location(stage):
    """Return the location name for the current stage."""
    if stage == 1:
        return "School Hallway Third Floor"
    if stage == 2:
        return "In Front Of The Iron Gate"
    if stage == 3:
        return "The Locked Iron Gate"
    if stage == 4:
        return "Hidden Staircase"
    if stage == 5:
        return "Outside The No Entry Room"
    if stage == 6:
        return "Inside The No Entry Room"
    if stage == 7:
        return "Hidden Laboratory Room"
    return "Unknown Location"


def print_title():
    """Display a simple ASCII title screen."""
    print("=" * 57)
    print("  _____ _            _                _            _  ")
    print(" |_   _| |__   ___  | |    ___   ___| | _____  __| |  ")
    print("   | | | '_ \ / _ \ | |   / _ \ / __| |/ / _ \/ _` |  ")
    print("   | | | | | |  __/ | |__| (_) | (__|   <  __/ (_| |  ")
    print("   |_| |_| |_|\___| |_____\___/ \___|_|\_\___|\__,_|  ")
    print()
    print("         S T A I R C A S E   C A S E")
    print()
    print("       An Interactive Investigation Game")
    print("=" * 57)
    print("        [ Evidence ]  [ Time ]  [ Choices ]")
    print("=" * 57)


def print_intro():
    """Display the introduction."""
    print("\nYou are Mo, a high school student.")
    print("\nAfter the morning classes end, at noon, you spot your classmate T,")
    print("who claims to be a detective, trying to pick the lock on an iron gate")
    print("in a side corridor on the third floor of the teaching building.")
    print("\nThe staircase behind it seems to lead to an unopened area of the")
    print("laboratory building that cannot be accessed from the main entrance.")
    print("\nWhat could be hidden inside?")
    print("\nYou have to find out what she is up to before the afternoon classes begin.")
    print("Otherwise, a teacher may discover you, and you will be forced to stop")
    print("your investigation and probably get into trouble.\n")


def show_status(state):
    """Display the current location, time left, and useful evidence list."""
    print("\n" + "-" * 68)
    print("Location:", get_location(state["stage"]))
    print("Time Left:", time_string(state["minutes_left"]))

    if len(state["evidence"]) == 0:
        print("Evidence Collected: []")
    else:
        print("Evidence Collected:")
        for item in state["evidence"]:
            print(" -", item)
    print("-" * 68)


def show_pending_output(state):
    """Display the story output from the previous player choice."""
    if state["pending_output"] != "":
        print(state["pending_output"])
        state["pending_output"] = ""
    return state


def get_menu_choice(options):
    """Display a numbered menu and read a valid choice from the player."""
    number = 1
    for option in options:
        print(str(number) + ". " + option)
        number = number + 1

    while True:
        try:
            choice = int(input("Choose an option: "))
            if choice >= 1 and choice <= len(options):
                return choice
            print("Please enter a number from 1 to", len(options))
        except ValueError:
            print("Invalid input. Please enter a number.")


def round_one_meet_t(state, log_file):
    """Decision point 1: Mo sees T at the locked gate."""
    print("What would you like to do?\n")
    options = [
        "Slip away and pretend you see nothing because you don’t want to mess around.",
        "Sneak up on her and ask what she is doing in Japanese (because she’s a super fan of the Japanese anime ‘Detective Conan’ and everyone in your class knows it.)",
        "Ask what she is doing loudly from the distance.",
        "Stop her because this is not right."
    ]
    choice = get_menu_choice(options)

    if choice == 1:
        state = spend_time(state, 5, "Mo tried to slip away", log_file)
        state["pending_output"] = (
            "It’s too late! She already saw you and calls your name. You have no choice but to step ahead.\n"
            "“Er, what are you doing?” you ask, a bit awkwardly.\n\n"
            "“Don’t you think this is intriguing?” She gives a sly smile.\n"
            "“Don’t you want to know where this leads to? By the way, according to my deduction, it’s a secret pathway towards the laboratory building--unopened area, the one we can’t access from the main entrance.”\n\n"
        )
    elif choice == 2:
        state = spend_time(state, 5, "Mo spoke to T in Japanese", log_file)
        state["pending_output"] = (
            "She seems surprised by you and answers promptly in Japanese, “Nothing,” while hiding her lock picking tools behind her back swiftly, before she realises to change language, “Wait, what are you doing here? And you can speak Japanese?”\n\n"
            "“Well, can’t you speak either?” You say, “So, why were you picking the lock?”\n\n"
            "“Don’t you think this is intriguing?” She gives a sly smile.\n"
            "“Don’t you want to know where this leads to? By the way, according to my deduction, it’s a secret pathway towards the laboratory building--unopened area, the one we can’t access from the main entrance.”\n\n"
        )
    elif choice == 3:
        state["noise"] = state["noise"] + 1
        state = spend_time(state, 5, "Mo called T from a distance", log_file)
        state["pending_output"] = (
            "She turns her head and sees you. She says, “Come, have a look at this locked staircase.”\n\n"
            "You move closer.\n\n"
            "“Don’t you think this is intriguing?” She gives a sly smile.\n"
            "“Don’t you want to know where this leads to? By the way, according to my deduction, it’s a secret pathway towards the laboratory building--unopened area, the one we can’t access from the main entrance.”\n\n"
        )
    else:
        state = spend_time(state, 5, "Mo tried to stop T", log_file)
        state["pending_output"] = (
            "“Come on, don’t be so serious,” T says, still blocking the lock picking tools behind her back.\n"
            "“I’m not stealing anything. I’m investigating. There is a difference.”\n\n"
            "You tell her that picking a lock is still not right.\n"
            "T lowers her voice and says, “Then stop me after you know what is behind this gate.”\n\n"
            "“Don’t you think this is intriguing?” She gives a sly smile.\n"
            "“Don’t you want to know where this leads to? By the way, according to my deduction, it’s a secret pathway towards the laboratory building--unopened area, the one we can’t access from the main entrance.”\n\n"
        )

    if not state["game_over"]:
        state["stage"] = 2

    return check_noise(state, log_file)


def round_two_decide_help(state, log_file):
    """Decision point 2: Mo decides whether to help T investigate."""
    print("You must decide whether to help T investigate the locked staircase.\n")
    options = [
        "Refuse to help and report T immediately.",
        "Agree to help, but only if you both collect real evidence.",
        "Question T first and ask why she suspects this staircase."
    ]
    choice = get_menu_choice(options)

    if choice == 1:
        state = spend_time(state, 15, "Mo reported T without evidence", log_file)
        state["pending_output"] = (
            "\nYou decide that this has gone too far and go to find a teacher.\n"
            "However, you have no real evidence of what T was trying to do.\n"
            "T denies that she entered anywhere, and the teacher only sees two students near a restricted corridor.\n"
            "The investigation ends before it even begins.\n\n"
        )
        if not state["game_over"]:
            state["game_over"] = True
            state["ending"] = "reported_too_early_failure"
            write_timed_log(log_file, state, "Ending reached: Mo reported T too early")
    elif choice == 2:
        state = spend_time(state, 10, "Mo agreed to investigate with T", log_file)
        state["pending_output"] = (
            "You agree to help, but you tell T that guessing is not enough.\n"
            "If there is really something hidden here, you need evidence that can prove it.\n"
            "T nods, looking more excited than worried.\n"
            "“Finally, someone understands the basic dignity of an investigation,” she says.\n\n"
        )
        state["stage"] = 3
    else:
        state = spend_time(state, 15, "Mo questioned T before helping", log_file)
        state["pending_output"] = (
            "T explains that an old school map once showed a connection between the teaching building and the laboratory building.\n"
            "The current map hides it completely, which means the staircase may have been sealed on purpose.\n"
            "“So your evidence is a missing line on a map?” you ask.\n"
            "“A missing line is sometimes more important than a printed one,” T says, completely serious.\n"
            "You are not fully convinced, but the hidden route is suspicious enough to check.\n\n"
        )
        state["stage"] = 3

    return check_noise(state, log_file)


def round_three_open_gate(state, log_file):
    """Decision point 3: The player chooses how to get through the iron gate."""
    print("The iron gate is old, but the lock has fresh scratches around it.")
    print("T thinks she can open it quietly, but there may be better ways to investigate.\n")
    options = [
        "Let T pick the lock quietly.",
        "Search around the gate for clues before opening it.",
        "Force the gate open quickly."
    ]
    choice = get_menu_choice(options)

    if choice == 1:
        state = spend_time(state, 20, "T quietly opened the gate", log_file)
        state = add_evidence(state, "fresh scratches around the lock", log_file)
        state["pending_output"] = (
            "T works carefully. The lock clicks open after a tense wait.\n"
            "Before she finishes, you notice fresh scratch marks around the lock that were already there.\n"
            "“See?” T whispers. “Someone else has been interested in this place too.”\n"
            "\nEvidence added: fresh scratches around the lock\n\n"
        )
    elif choice == 2:
        state = spend_time(state, 25, "Mo searched around the gate", log_file)
        state = add_evidence(state, "old access notice about a restricted storage room", log_file)
        state["pending_output"] = (
            "You search the wall and find part of an old access notice under faded tape.\n"
            "It mentions a laboratory annex and a restricted storage room.\n"
            "T leans over your shoulder. “Restricted storage room. That sounds better than lunch.”\n"
            "“That is not a normal standard,” you say.\n"
            "\nEvidence added: old access notice about a restricted storage room\n\n"
        )
    else:
        state["noise"] = state["noise"] + 2
        state = spend_time(state, 15, "Mo forced the gate open", log_file)
        state = add_evidence(state, "fresh scratches around the lock", log_file)
        state["pending_output"] = (
            "You push the gate hard. The metal gives a loud cry.\n"
            "The gate opens, but the noise echoes through the corridor.\n"
            "T freezes for a second. “That was the least detective-like method possible.”\n"
            "\nEvidence added: fresh scratches around the lock\n\n"
        )

    if not state["game_over"]:
        state["stage"] = 4

    return check_noise(state, log_file)


def round_four_staircase(state, log_file):
    """Decision point 4: Investigation on the hidden staircase."""
    print("Behind the gate, a narrow staircase leads toward the laboratory building.")
    print("Dust covers most of the steps, but not all of them.")
    print("Somewhere below, the air smells faintly sharp and chemical.\n")
    options = [
        "Inspect the dusty steps and footprints.",
        "Read the faded notice board on the landing.",
        "Follow the strange chemical smell coming from below."
    ]
    choice = get_menu_choice(options)

    if choice == 1:
        state = spend_time(state, 15, "Mo inspected the dusty staircase", log_file)
        state = add_evidence(state, "fresh footprints on the hidden stairs", log_file)
        state["pending_output"] = (
            "You find fresh footprints in the dust. Someone else has used this route recently.\n"
            "T crouches beside you. “Recent footprints. Good. The staircase is not just old school decoration.”\n"
            "\nEvidence added: fresh footprints on the hidden stairs\n\n"
        )
    elif choice == 2:
        state = spend_time(state, 15, "Mo read the old safety notice", log_file)
        state = add_evidence(state, "old safety notice about specimen storage", log_file)
        state["pending_output"] = (
            "The notice board says that part of the laboratory building was closed after a safety inspection.\n"
            "One line mentions temporary specimen storage, but the date is many years old.\n"
            "“Temporary for several years,” you mutter. “Very efficient.”\n"
            "T smiles. “Suspicious efficiency is still suspicious.”\n"
            "\nEvidence added: old safety notice about specimen storage\n\n"
        )
    else:
        state = spend_time(state, 20, "Mo followed the chemical smell", log_file)
        state = add_evidence(state, "recent chemical smell from the laboratory annex", log_file)
        state["pending_output"] = (
            "You follow the chemical smell downward into the laboratory annex.\n"
            "The smell is faint but recent, as if a container was opened not long ago.\n"
            "T covers her nose. “This is becoming much less romantic as an adventure.”\n"
            "\nEvidence added: recent chemical smell from the laboratory annex\n\n"
        )

    if not state["game_over"]:
        state["stage"] = 5

    return check_noise(state, log_file)


def round_five_enter_room(state, log_file):
    """Decision point 5: The player chooses whether to enter the No Entry room."""
    print("You and T reach an old laboratory corridor that is not shown on the normal school map.")
    print("At the end of the corridor, one door has a sign that says: NO ENTRY.")
    print("The door is not locked. That makes it feel stranger, not safer.\n")
    options = [
        "Enter the NO ENTRY room with T.",
        "Hesitate at the sign and check the area beside the door first.",
        "Leave now and report the corridor without going inside."
    ]
    choice = get_menu_choice(options)

    if choice == 1:
        state = spend_time(state, 15, "Mo entered the No Entry room with T", log_file)
        state = add_evidence(state, "recent trace on the No Entry room door handle", log_file)
        state["pending_output"] = (
            "You open the door. A cold chemical smell rolls out from the room.\n"
            "T steps in first, then looks back at you. “Come on. This is exactly the kind of room detectives enter.”\n"
            "You sigh and follow her. The door handle has a cleaner patch than the rest of the dusty door.\n"
            "\nEvidence added: recent trace on the No Entry room door handle\n\n"
        )
        state["stage"] = 6
    elif choice == 2:
        state = spend_time(state, 20, "Mo hesitated and checked the No Entry doorway", log_file)
        state = add_evidence(state, "biological specimen storage label", log_file)
        state["pending_output"] = (
            "You point at the sign and say that it literally says NO ENTRY.\n"
            "T answers, “For a detective, the more a place says not to enter, the more it needs to be entered.”\n"
            "That logic is dangerous, but unfortunately not boring.\n"
            "Before entering, you notice a faded label near the door: Biological Specimen Storage.\n"
            "\nEvidence added: biological specimen storage label\n\n"
        )
        state["stage"] = 6
    else:
        state = spend_time(state, 10, "Mo left before entering the No Entry room", log_file)
        state["pending_output"] = (
            "\nYou decide not to enter the room. Instead, you report that there is an unlocked room in a sealed corridor.\n"
            "Without seeing what is inside, your explanation sounds too vague.\n"
            "The corridor is locked again, and you are told not to create stories about restricted areas.\n\n"
        )
        if not state["game_over"]:
            state["game_over"] = True
            state["ending"] = "unproven_room_failure"
            write_timed_log(log_file, state, "Ending reached: Mo left before entering the room")

    return check_noise(state, log_file)


def round_six_footsteps(state, log_file):
    """Decision point 6: Someone approaches while Mo and T are inside."""
    print("Inside the room, shelves and covered boxes stand in uneven rows.")
    print("Before you can inspect them properly, footsteps sound from the corridor outside.")
    print("T immediately raises one finger to her lips.\n")
    options = [
        "Hide behind the old storage shelves and wait.",
        "Run out of the room before the person arrives.",
        "Keep searching quickly because there is no time to waste."
    ]
    choice = get_menu_choice(options)

    if choice == 1:
        state = spend_time(state, 20, "Mo and T hid from the footsteps", log_file)
        state["pending_output"] = (
            "You and T squeeze behind the shelves. Dust gets into your nose, but you try hard not to sneeze.\n"
            "Someone stops outside the door for a moment, then walks away.\n"
            "T gives you a silent thumbs-up. You are not sure whether to feel proud or ridiculous.\n\n"
        )
        state["stage"] = 7
    elif choice == 2:
        state["noise"] = state["noise"] + 2
        state = spend_time(state, 10, "Mo and T tried to run from the footsteps", log_file)
        state["pending_output"] = (
            "\nYou rush toward the door, but the sudden movement makes a box scrape loudly across the floor.\n"
            "The person in the corridor hears it and comes straight to the room.\n\n"
        )
        if not state["game_over"]:
            state["game_over"] = True
            state["ending"] = "caught_failure"
            write_timed_log(log_file, state, "Ending reached: Mo and T were discovered while running")
    else:
        state["noise"] = state["noise"] + 2
        state = spend_time(state, 10, "Mo kept searching despite the footsteps", log_file)
        state["pending_output"] = (
            "\nYou keep searching, but the jars clink softly when you move a cloth aside.\n"
            "T whispers, “Mo, that sound was not part of my plan.”\n"
            "The footsteps stop outside the door.\n\n"
        )
        if not state["game_over"]:
            state["game_over"] = True
            state["ending"] = "caught_failure"
            write_timed_log(log_file, state, "Ending reached: Mo and T were discovered while searching")

    return check_noise(state, log_file)


def has_supporting_evidence(state):
    """Return True if the player has collected a clear evidence trail."""
    evidence = state["evidence"]
    gate_evidence = "fresh scratches around the lock" in evidence or "old access notice about a restricted storage room" in evidence
    stair_evidence = "fresh footprints on the hidden stairs" in evidence or "old safety notice about specimen storage" in evidence or "recent chemical smell from the laboratory annex" in evidence
    room_evidence = "recent trace on the No Entry room door handle" in evidence or "biological specimen storage label" in evidence
    photo_evidence = "photos of the prohibited snake specimens" in evidence
    return gate_evidence and stair_evidence and room_evidence and photo_evidence


def round_seven_phone_photo(state, log_file):
    """Decision point 7: The player chooses whether to take photos with the forbidden phone."""
    print("After the footsteps fade away, you finally pull the cloth from one shelf.")
    print("Rows of glass jars appear in front of you.")
    print("Inside the jars, many snakes are preserved in formalin.")
    print("T stares at them for several seconds.")
    print("“I know this is bad,” she says, “but I have no idea what kind of snakes these are.”")
    print("You remember an illustrated animal encyclopedia you once read and recognise the pattern on several of them.")
    print("Some of these snakes are nationally protected animals.")
    print("This is no longer just a strange hidden room. It is evidence of prohibited specimens.")
    print("\nSchool rules forbid students from carrying phones, but you secretly have yours with you.")
    print("If you use it now, you may get proof. You may also get yourself into trouble.\n")

    state = add_evidence(state, "prohibited snake specimens in formalin", log_file)

    options = [
        "Take out your forbidden phone and photograph the jars.",
        "Do not use the phone. Memorise the details and report them later.",
        "Leave the room quietly with T and keep the discovery secret for now."
    ]
    choice = get_menu_choice(options)

    if choice == 1:
        state["phone_used"] = True
        state = spend_time(state, 25, "Mo used the forbidden phone to take photos", log_file)
        state = add_evidence(state, "photos of the prohibited snake specimens", log_file)
        state["pending_output"] = (
            "\nYou take photos of the jars, the shelf labels, the NO ENTRY sign, and the old corridor outside.\n"
            "T watches the door for you. When you put the phone away, she says quietly,\n"
            "“I won’t tell anyone you brought it. A detective protects useful witnesses.”\n"
            "“Since when am I your witness?” you ask.\n"
            "“Since you became useful,” she says. “Detective assistant also works, if you prefer that title.”\n"
            "\nEvidence added: photos of the prohibited snake specimens\n\n"
        )

        if not state["game_over"]:
            if has_supporting_evidence(state):
                state["game_over"] = True
                state["ending"] = "success"
                write_timed_log(log_file, state, "Ending reached: successful investigation")
            else:
                state["game_over"] = True
                state["ending"] = "partial_success"
                write_timed_log(log_file, state, "Ending reached: partial success with photos but weak supporting evidence")
    elif choice == 2:
        state = spend_time(state, 15, "Mo decided not to use the forbidden phone", log_file)
        state["pending_output"] = (
            "\nYou decide not to risk using your phone. You try to memorise the room, the shelves, and the labels.\n"
            "T looks at you for a moment, then says, “A detective without proof is just a storyteller.”\n"
            "When you report it later, your words are serious but not strong enough as proof.\n"
            "By the time the room is checked, the most suspicious jars have already been moved.\n\n"
        )
        if not state["game_over"]:
            state["game_over"] = True
            state["ending"] = "no_photo_failure"
            write_timed_log(log_file, state, "Ending reached: Mo did not take photo evidence")
    else:
        state = spend_time(state, 5, "Mo and T left without reporting", log_file)
        state["pending_output"] = (
            "\nYou and T leave the room quietly.\n"
            "You know something is wrong, but without action or evidence, the hidden room remains hidden.\n"
            "T looks frustrated, and neither of you says much on the way back to class.\n\n"
        )
        if not state["game_over"]:
            state["game_over"] = True
            state["ending"] = "secret_kept_failure"
            write_timed_log(log_file, state, "Ending reached: Mo kept the discovery secret")

    return check_noise(state, log_file)


def show_ending(state):
    """Display the final ending based on the game state."""
    print("\n" + "=" * 68)

    if state["ending"] == "success":
        print("SUCCESS ENDING: THE HIDDEN SPECIMENS EXPOSED")
        print("You call the police and show the photos, then explain how the locked staircase leads to the hidden laboratory room.")
        print("The prohibited snake specimens in formalin can no longer be dismissed as a rumour or a student prank.")
        print("T keeps her promise and does not tell the teachers that you secretly brought your phone to school.")
        print("When the police take over the scene, the two of you finally realise that lunch is completely gone.")
        print("On the way back to class, T walks beside you and says, “Mo, you noticed things I missed.”")
        print("Then she smiles. “So, from now on, would you like to keep working on investigations with me?”")
        print("You do not answer immediately, but you also do not say no.")
    elif state["ending"] == "partial_success":
        print("MIXED ENDING: PHOTOS WITHOUT A FULL TRAIL")
        print("Your photos prove that the hidden room exists and contains prohibited specimens.")
        print("However, because your other evidence is weak, it is harder to explain how the room was being used recently.")
        print("T still protects your phone secret, but the case feels less complete than it should.")
    elif state["ending"] == "time_failure":
        print("FAILURE ENDING: TOO LATE")
        print("Afternoon classes begin before you can finish the investigation.")
        print("A teacher finds you outside the classroom and orders you back immediately.")
        print("Your investigation is forced to stop.")
    elif state["ending"] == "caught_failure":
        print("FAILURE ENDING: DISCOVERED")
        print("The noise brings someone to the restricted corridor.")
        print("You and T are caught before you can collect enough evidence.")
        print("The investigation ends with trouble instead of a solution.")
    elif state["ending"] == "reported_too_early_failure":
        print("FAILURE ENDING: TOO EARLY TO REPORT")
        print("You reported T before finding out what the staircase hides.")
        print("Without evidence, the situation looks like two students causing trouble near a restricted area.")
        print("The truth remains behind the iron gate.")
    elif state["ending"] == "unproven_room_failure":
        print("FAILURE ENDING: THE ROOM YOU DID NOT ENTER")
        print("You found the hidden corridor, but you did not enter the NO ENTRY room.")
        print("Without knowing what was inside, you cannot prove the real problem.")
        print("The door is closed again before anyone takes your report seriously.")
    elif state["ending"] == "no_photo_failure":
        print("FAILURE ENDING: NO PROOF")
        print("You saw the protected snake specimens, but you did not take photo evidence.")
        print("Your memory is not enough to prove what was hidden in the room.")
        print("By the time the adults check, the most important evidence is gone.")
    elif state["ending"] == "secret_kept_failure":
        print("FAILURE ENDING: THE SECRET STAYS HIDDEN")
        print("You and T leave without reporting the hidden room.")
        print("The strange room remains sealed away, and the truth stays inside it.")
    else:
        print("GAME OVER")
        print("The investigation ends without a clear result.")

    print("=" * 68)
    print("Final Evidence Collected:")
    if len(state["evidence"]) == 0:
        print(" - None")
    else:
        for item in state["evidence"]:
            print(" -", item)
    print("=" * 68)


def play_game():
    """Run the main game loop."""
    log_file = create_new_log_file()
    state = create_initial_state()

    start_log(log_file)
    print_title()
    print_intro()
    input("\nPress Enter to begin the investigation...")

    while not state["game_over"]:
        show_status(state)
        state = show_pending_output(state)

        if state["stage"] == 1:
            state = round_one_meet_t(state, log_file)
        elif state["stage"] == 2:
            state = round_two_decide_help(state, log_file)
        elif state["stage"] == 3:
            state = round_three_open_gate(state, log_file)
        elif state["stage"] == 4:
            state = round_four_staircase(state, log_file)
        elif state["stage"] == 5:
            state = round_five_enter_room(state, log_file)
        elif state["stage"] == 6:
            state = round_six_footsteps(state, log_file)
        elif state["stage"] == 7:
            state = round_seven_phone_photo(state, log_file)
        else:
            state["game_over"] = True
            state["ending"] = "unknown"
            write_timed_log(log_file, state, "Unexpected stage reached")

    state = show_pending_output(state)
    show_ending(state)
    write_timed_log(log_file, state, "Game ended with result: " + state["ending"])
    print("\nA playthrough log has been saved to", log_file)


def ask_play_again():
    """Ask the player whether to restart or quit after an ending."""
    print("\n\nCase closed! What would you like to do next?\n")
    options = [
        "Play again.",
        "Quit."
    ]
    choice = get_menu_choice(options)
    return choice == 1


def main():
    """Run the game and allow the player to replay after each ending."""
    playing = True

    while playing:
        play_game()
        playing = ask_play_again()

        if playing:
            print("\nRestarting the investigation...\n")
        else:
            print("\nThank you for playing.")


main()