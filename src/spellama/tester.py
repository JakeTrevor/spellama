test_cases =[
    ("To them these conditions felt like the embrace of an old lover, something familiar, almost homely in its misery.","To them, these conditions felt like the embrace of an old lover — something familiar, almost homely in its misery."),
    ("Heavy, armoured steps threw up mud in little waves, every step a personal apocalypse for the small creatures that called this field their home.","Heavy, armoured steps threw up mud in little waves — every step a personal apocalypse for the small creatures that called this field their home"),
    ("The men were marched, armed with a wild mix of greatswords, polearms, warhammers and of course pistols - barrels sealed with beeswax to keep out the moisture.","The men were marched, armed with a wild mix of greatswords, polearms, warhammers, and, of course, pistols — barrels sealed with beeswax to keep out the moisture."),
    ("It was all in all a clever trick though: disguise yourself to fool the scouts and then cleanly punch through the poor idiots you face.","It was, all in all, a clever trick though: disguise yourself to fool the scouts and then cleanly punch through the poor idiots you face."),
    ("_","If they fired now — so he thought — they would be trying for a second volley, impossible in the rain."),
    ("Merridew had never had a formal education and while he had learned to read as an adult he had never bothered to learn the heraldry and customs of their neighbours hell, he barely knew the banners he marched to war under.","Merridew had never had a formal education, and while he had learned to read as an adult, he had never bothered to learn the heraldry and customs of their neighbours — hell, he barely knew the banners he marched to war under."),
    ("So he shared his little canopy with a corpse and a murderer and wondered what exactly the evening would bring.","So he shared his little canopy with a corpse and a murderer, and wondered what exactly the evening would bring."),
    ("Barnabas felt a little strange looking at the dead bird, somehow the presence of the human corpse nearby made him feel uneasy at the thought of cooking flesh.","Barnabas felt a little strange looking at the dead bird; somehow, the presence of the human corpse nearby made him feel uneasy at the thought of cooking flesh."),
    ('Barnabas did not quite believe her. "Aye that you did but you don\'t seem such a stranger to insult."','Barnabas did not quite believe her. "Aye, that you did, but you don\'t seem such a stranger to insult."'),
    ('"Four of us, one chicken you see and as it is still cooking I\'m quite afraid I will want to hear your story in advance."','"Four of us, one chicken you see — and as it is still cooking, I\'m quite afraid I will want to hear your story in advance."'),
]



from MistralCorrectV_2 import MistralCorrector_V2

correctors = [MistralCorrector_V2]

def test():
    corrector:MistralCorrector_V2 = MistralCorrector_V2() #type: ignore
    print("============================")
    print("Testing "+corrector.__class__.__name__)
    print("============================")
    print("Testing positives")
    count = 0
    total = 0
    for i in test_cases:
        total = total+1
        res = corrector.check(i[1])

        if res:
            count = count+1
        else:
           print("===fail===")
           print(i[1])
           print(res)
    print(count)
    print(total)
    print("============================")
    print("Testing negatives")
    total = 0
    count = 0
    for i in test_cases:
        if i[0] != "_":
            total = total+1
            res = corrector.check(i[0])

            if not res:
                count = count+1
            else:
               print("===fail===")
               print(i[0])
               print(res)
               
    print(count)
    print(total)

    print("=======================")
    print("Testing self correction")
    
    for i in filter(lambda x: x[0] !="_",test_cases):
       res = corrector.correct(i[0])
       if not res==i[1]:   
        print("====NOT HIT====")
        print("====ORIGINAL====")
        print(i[0])
        print("====CORRECTION====")
        print(res)
        print("====TARGET====")
        print(i[1])
       else:
          print("hit")


    corrector.llm.close()
        

test()