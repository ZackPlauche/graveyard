<template>
  <div>
    <!-- Header -->
    <header class="min-h-screen-navbar flex flex-col bg-cover bg-right bg-no-repeat p-5 bg-[url('/zack-batumi.jpg')]">
      <div class="flex-1 max-w-7xl flex items-center w-full mx-auto">
        <div>
          <!-- Content -->
          <h1 class="text-9xl font-serif text-white">About Zack</h1>
          <p class="text-white text-5xl font-extralight">Scroll down.</p>
        </div>
      </div>
    </header>

    <!-- About Section Content -->
    <section class="px-10 pb-10">

      <!-- Intro Paragraph -->
      <p class="text-2xl text-gray-700 leading-10 text-center max-w-5xl mx-auto font-normal mt-20"><span class="inline-block text-5xl font-semibold hover:animate-bounce md:text-2xl">Hi!👋</span>Welcome to my website. <br><br>My name is Zack Plauché. I love being healthy, making music, developing software, and teaching people useful life skills that bring them awesome results. <br><br> <span class="font-bold">I'm here to change shit and make the world a better place.</span> <br><br>I believe the world needs more good, strong, and smart people. And, I want to help develop those people and help them achieve epic results in their own lives and positively impact the lives of others.</p>

      <!-- Values Section -->
      <section class="text-center mt-20">
        <h2 class="mt-3">Values</h2>
        <p class="mt-2">The driving forces behind everything that I do.</p>

        <!-- Values List -->
        <div class="flex gap-x-6 gap-y-10 flex-wrap justify-center mt-7">
          <ValueCard v-for="value in topValues" :key="value.name" :value="value" />
        </div>
      </section>

      <!-- Team Section -->
      <!-- <section class="mt-20 mx-auto max-w-6xl">
        <h2 class="text-center">My Team</h2>
        
        <div class="grid grid-cols-6">

          <div class="col-span-2">

            <div class="border w-full rounded-2xl py-10 px-5">

              <div class="aspect-square h-[200px] rounded-full mx-auto overflow-hidden">
                <img class="h-full w-full object-cover object-center" src="/zack-pro-dev.jpg">
              </div>
              
              <div class="text-center mt-5">

                <h3 class="text-5xl font-serif text-blue-dark">Zack Plauché</h3>

                <h4 class="text-xl mt-2 font-medium text-gray-600">King of the Kingdom</h4>

                <p class="mt-5">Chief Everything Officer of the Zack Plauché brand. He likes to make music, build software and businesses, cook & eat healthily, workout, and spend time with friends.</p>

              </div>
              
            </div>
          </div>

          <div>

          </div>

        </div>

      </section> -->


      <!-- My Story -->
      <section class="mx-auto prose prose-h3:text-blue-dark prose-ol:font-semibold prose-ul:font-semibold mt-14">
        <h2 class="mb-0 text-center">My Story</h2>
        <!-- Last updated -->
        <div class="text-sm text- font-light text-center mt-4">Last updated: January 2020</div>
        <h3 class="text-2xl text-blue-dark mt-4 text-center">Warning: This is a lot of text.</h3>
        <p>Once upon a time, in the land of Mississippi, there was a hospital where a boy was born.</p>
        <p>This wasn't any ordinary boy. This boy was a bit different than most of the other southern raised boys &amp; girls... He just didn't know it yet.</p>
        <p>His parents had the option of naming him whatever they wanted. His father was thinking about calling him "Pierre" or "Maximillian".
          Luckily his mother was there to save him from these names and gave him the super cool name of "Zachary". Zachary Plauche.</p>
        <p>For the sake of the story, we'll refer to Zachary Plauche as "Zack Plauché" due to the main characters preferences.
          And since the main character is the one writing this story on his own website, my <i>**ahem**</i> I mean his word is final.</p>
        <p>Having grown up in Mississippi, as a young boy Zack didn't know a lot about the world. Unless of course by the world you mean the world of videogames. He knew quite a lot about those.</p>
        <p>Zack was never really good in school, except in a few random areas. He was really good at spelling, english, and math. Well, initially math. He was actually in advanced placement until he had to show his work.
          For some reason, he was a lot better at math when he could do it in his head. One year in high school his teacher was not very good at her job, so his advancement in math got paused for the rest of his school life.</p>
        <p>Here's a quick flash of what he remembers before his life really got interesting:</p>
        <ol>
          <li>He went to a catholic school for about 3 years.</li>
          <li>There was a big hurricane called Katrina that hit his home town when he was 8.</li>
          <li>He went to Pass Christian School for the rest of his school life.</li>
          <li>He had a lot of crushes in school but was too socially awkward to talk to them. He did ask them out sometimes, but those efforts typically failed.</li>
          <li>He had his first girlfriend when he was 16 (she wasn't from Mississippi, she was from Colorado).</li>
          <li>After the short lasting first relationship he fell into a clinical depression.</li>
          <li>He realized school was pretty much pointless.</li>
          <li>He learned to give up Christianity (he really didn't know there was another option until later)</li>
          <li>His sheep guidance counselor told him he was going to college. She was wrong.</li>
        </ol>
        <p>She was very wrong.</p>
        <h3>2015</h3>
        <p>Zack graduated high school at 17 years old and really had no intention of going back to school. "Fuck that entirely" he exclaimed. More than once. It wasn't really an option for him. His grades were pretty average, and while he could've gone to the normal community college, he decided just to work.</p>
        <p>Before we continue, let's go over what Zack started out with upon entering the real world:</p>
        <ul>
          <li>He was diagnosed with depression and anxiety.</li>
          <li>He had his first job (working at Subway franchise restaurant at the Walmart in front of his house).</li>
          <li>No car.</li>
          <li>No plan of going to college.</li>
        </ul>
        <p>Ok, that's not exactly a great start. But what did he have?</p>
        <ul>
          <li>He had started learning about Self-Development when he turned 15 when he decided to learn "Pickup" by first googling "How to get a girlfriend".</li>
          <li>He had a pretty positive and outgoing personality (the days varied when it was real or forced).</li>
          <li>A phone.</li>
          <li>A pretty good resource with insights on how to get out of depression.</li>
        </ul>
        <p>Zack was pretty funny. His senior year of high school he had a therapist because he felt he needed one. He also learned about a really awesome book on health called "The Ultramind Solution" by Dr. Mark Hyman from one of the Pick Up gurus he was learning from. While he was still getting therapy, he was telling his therapist about this amazing book and the plan of how to get out of his depression. His therapist was actually really inspired by everything Zack was doing, bought a copy of the book, and said that he'll probably be an inspiration to people one day. Zack goes to therapist. Zack leaves with the therapist inspired.</p>
        <p>One thing you should know, the "learning pickup" phase was a really weird and lonely part of Zack's life that he was lucky enough to eventually have pulled out of thanks to one of his mentors he met at a later point. It didn't have to be that hard, but in school there really weren't any classes appropriately be called "How to Communicate Clearly". That would've been great. Anyways, let's continue.</p>
        <p>Soon enough, Zack's bubbly personality attracted the attention of Sean Pittman, the owner of probably the only contemporary place that existed in Mississippi: Cat Island Coffeehouse. This was a HUGE step-up for Zack, and about a $0.75 increase in pay! ($8 an hour was a lot of money to Zack in 2015 #mississippimindset).</p>
        <p>The environment at the coffeehouse was amazing. It was clean, organizeed, and filled with books, coffee, and it's where Zack met his second love: Matcha green tea.</p>
        <p>Zack met Matcha before when he was spending time with his first girlfriend, he just didn't know Matcha's real name at the time. He only knew her back then as "Green Tea Frappaccino from Starbucks' secret menu". Matcha is the healthiest green tea on the planet with 10x more antioxidants the closest green tea concentration. If you ever decide to make matcha properly, you'll need a bamboo whisk, a bowl, and hot water. Specifically, you'll need hot water at exactly 165 degrees fahrenheit, otherwise you'll burn it and it'll taste bitter, or it'll be too watery. This whole paragraph about Matcha might sound off topic, but Zack has enjoyed this beautiful green creation for years. And at the time this story is being written (Febuary 28th, 2020), he still enjoys a hot matcha latté almost daily. The experience he gets from this drink is somewhere along the lines of the russian word оргастический. You can look that up on your own time.</p>
        <p>Cat Island Coffeehouse is also where Zack met his first roommate, Robert. One of Zack's first goals upon entering the real world was leaving his parents house, and he did so not even a year later after graduating.</p>
        <p>You learn a lot working at a coffeehouse. Before Zack worked here, he had literally had no idea there were more types of tea than just sweet or unsweet. I know what you're thinking "Whaaaaat? There's more tea than just sweet or unsweet?". I know. I thought the same.</p>
        <p>Zack liked working there because he finally had a real support network. Most everyone who worked there was really cool, and Sean was kind of Zack's first mentor type person in his life. Or maybe good friend. Sean was the first person to openly share to Zack that there was something special about him and that he had potential to do great things.</p>
        <p>Throughout this time, Zack was still working on curing his own depression. With the Ultramind Solution as his mental health bible, Zack decided to try out some more of the recommendations beyond just exercise (exercise, mostly running, was the initial main thing Zack did to move towards curing his clinical depression, because it was pretty much free, and he didn't have the skills or financial resources to eat a lot of health food). The suggestion Zack wanted to try required an old medicine that was very new to him, which was essential oils. He sought out an herbalist, which he had no idea if they even existed in Mississippi. Turns out, they did. Enter Lynda Baker.</p>
        <p>
          Lynda (or Miss Lynda as he and a lot of others called her) is one of the most kind hearted, loving, funny, brilliant older women Zack has ever met. She immiediately liked Zack (even though he was initially uncomfortable upon meeting her at her store. The place was a mess at first.) and was super friendly and welcoming. Zack was a bit off put, but open minded and continued his journey to get essential oil, and he did! Along with some free soaps that Miss Lynda gave him. Lynda immediately was sharing the tip of the iceburg of what I later found to be her vast knowledge of herbalism and holistic medicine. Zack would visit a couple more times to make more purchases, but because he wasn't making much money, he came up with another idea. He sent her a message "Hey Miss Linda! I'd love to clean your store and in exchange you teach me what you know about herbalism". She had a problem. I had a solution. She shared so many amazing things with me, taking me on Herb Walks, to other herb cottages, teaching me about different god type figures like Krishna and Buddha. And the medicines and herbs she shared with me were nothing short of magic. One time she made Zack a sleep tincture made from Passionflower, Valerian Root, &amp; Life Everlasting. Imagine if NyQuil didn't pretty much force your body to go to sleep, and instead was like "Hey, you can go to sleep now if you'd like. Or you could stay up. It's up to you." and also wasn't like drinking a cap full of medicine sugar syrup. That's what this magical concoction was. Almost a years worth of shitty sleep and insomnia pretty much gone in a few drops of this natural medicine.
        </p>
        <p>After realizing how powerful this natural medicine was, Zack became really inspired that this type of medicine was out there and that barely any people really know how to use it. Lynda was and still is a literal master herbalist that inspired Zack and helped him build part of his vision.</p>
        <p>Speaking of vision, it was around this time Zack had his first glimpse of a vision besides what felt to him like a pre-determined destiny for greatness. Zack was so frustrated that he even had to figure out this whole depression thing, because all everyone ge talked to about it with was telling him was "You just have it forever and learn to live with it", and he knew that couldn't be true. Zacl had his first glimpse of a vision. A vision of the kind of impact he wanted to make on the world. He formulated the idea that he wanted to make some kind of integrative health center that was going to make optimal health more popular and easy to access for people at all income levels. That's a sexy one liner for a mission statement right?</p>
        <h3>2016</h3>
        <p>Zack continued working at the coffeehouse until his roommate decided to move out. At this point, Zack's goal was to leave Mississippi, and he succeeded. He knew that where he needed to be wasn't in the hell hole that Missippi really was. After saying goodbye to his amazing friends he made there, he finally left.</p>
        <p>Zack bounced around the south to a few places only to realize what he was looking for wasn't just not in Mississippi, it wasn't in <a href="https://web.archive.org/web/20201022150258/https://en.wikipedia.org/wiki/Bible_Belt">the Bible Belt</a> at all. He went from Mississippi, to Georgia for a few months, then to a little town in Alabama called Fairhope. Funny enough, it was here in Fairhope that Zack had temporarily become the literal stereotype of a person who didn't go to college by getting a job at McDonalds. To Zack, the self-development health guy who's mission was to cure his depression through healthy lifestyle, this was a hell. Somehere aroudn this time was exactly when Zack realized his life still wasn't where he wanted it to be, but it wasn't actually horrible. Fairhope was kind of like a proverbial launch pad for Zack. He gave his car back to his parents and he was staying at his grandparents house to save money, a lot of money at the time. He realized, still, that the south wasn't where he needed to be. Fairhope was probably the best place he'd been by far, but it was too slow. There wasn't enough going on and the town was filled with mostly old people. Maybe later it would be cool, maybe, but right now it wasn't the place.</p>
        <p>During his time at McDonalds, there were 2 key events that made a massive impact on his life, and both were part of a larger strategy of growth.</p>
        <ol>
          <li>Zack had purchased a smart phone with the main intention of using audible to read a fuck ton of audiobooks, and since he could walk everywhere, he absolutely did.</li>
          <li>Zack had created a plan to leave.</li>
        </ol>
        <p>Zack had developed some criteria for where he was going to go. Because he wanted to mostly improve his networking and dating skills, it had to be a place with a lot of people. The second criteria, since he gave up his car, is that it needed to be walkable. The last thing, which was just an ideal, is that it needed to be a big city.</p>
        <p>After a lot of research, Zack decided that his first step outside of the bible belt would be directly to Sin City, a.k.a Las Vegas, Nevada.</p>
        <h3>2017</h3>
        <p>Shortly after this time period, Zack was saved from his job at McDonald's by this health food restaurant close by he would always go during his break time at McDonalds. They hired him, but there was a problem at first where I could only work part time because he needed to keep his job at McDonalds for money. Zack's boss at the health food restaurant got him to work there full time by saying "If you quit your job at McDonalds I'll pay you $10 an hour". Zack immediately called McDonald's management and told them he wasn't coming back. It was at the health food restaurant that Zack was surrounded by health food every single day. Real, organic, non-gmo, real super tastey quality food every single day. With Zack's goal of clearing out his depression, this was a dream job.</p>
        <p>It was around this time that Zack's depression pretty much went away completely. With a pretty heatlhy lifestyle, really decent income, and a growing perspective from all the books he was reading, the thing that actually put the nail in the coffin for this round of depression was the book Awaken The Giant Within by Tony Robbins (a book that his yoga mentor Megrez was reading at the time. For the record, Megrez was and still is awesome.)</p>
        <p>
          In Febuary of 2017, Zack's Dad invited him to go to Mardigras in New Orleans for a few days. Zack accepted this invitation, and in this decision Zack was soon to make one of the most important connections of his life. Through 3 days of meeting random people, some intentional people like Devin Ladner, Zack met a really cool and different group of people by drunkedly, in a controlled manner, hitting on a hot girl in a group. What looked to be the girls boyfriend soon walked up and was acting all macho, but this Zack was a lot more charismatic than he was when he was younger, and ended up making friends with both of them. It was a really short interaction, and basically he asked them "What are you guys up to tonight?". They told him they were going to some bar on some street Zack heard of that wasn't too far away. After the conversation ended Zack was sure he wasn't going to see those people again. He did end up going to that bar later though. There was a pretty massive crowd outside this place with a DJ booth and lots of people dancing (all on the street). He decided to enjoy the energy and dance with a few girls there. All of a sudden, in the massive crowd of loud music and dancing people, a highly improbable tap on the shoulder occured on Zack's shoulder that caused him to turn around. "Holy Shit." Zack said as he saw the girl who he was obviously hitting on earlier greeting him. To Zack it felt like sometihng out of a movie. She lead him to her group of 4 (including her). There was her, a well-dressed british guy, a jacked black guy who wore glasses, and the black guy's brown haired girlfriend. At least, a surface level that's what he saw. What I soon found was that everyone in this group were really awesome people.
        </p>
        <p>Now, which one of these 4 people was the important connection that Zack made that night? Was it:</p>
        <ol type="a">
          <li>The girl Zack hit on.</li>
          <li>The well dressed british guy</li>
          <li>The jacked black guy who wore glasses</li>
          <li>The brown haired girl</li>
        </ol>
        <p>The answer? It was the jacked black guy who wore glasses, and his name was Anand Houston.</p>
        <p>Zack actually had no idea that that connection would be so important. He left after about 2 hours of hanging out with them, mostly because Zack felt like if he stayed there at the time they'd realize they don't like eventually not like him.. This was mostly just due to shitty self-belief Zack had at the time, though he did add them on Facebook. Later he would hear from Anand that they wondered why he left. Either way, after hanging out with them, Zack felt super charged. It was one of the most amazing nights of Zack life, and just knowing amazing people like that group were out there reassured Zack that whatever path he was on, he was on the right one.</p>
        <p>Zack came back to Fairhope to work at the Health Food store a few more months until he finally left to Vegas, exactly as he planned.</p>
        <p>Vegas was interesting to say the least. There's nothing like landing in a desert city at a record high temperature of 118F and having the hairs in your nose disentegrate in the heat. Also, the morning after his first night in Vegas, Zack was walking on the strip (the main street in Vegas where all the massive casinos are on) at about 7am and a guy immediately offered him to buy cocaine. "What a friendly city!" Zack thought.</p>
        <p>Zack had enough cash to at least get sustainable upon his arrival there. His plan was to get there and either learn to survive on his own or die trying. There was a point and some pretty uncomfortable situations where Zack was almost homeless, but luckily he was able to eventually sort those out and be legally renting his own apartment. Zack got a few more normal jobs in retail and restaurants, and he was getting burnt out from all of them.</p>
        <p>A night before Zack was about to quit his job at Peppermill, the universe finally decided to give him a break. Re-Enter Anand Houston.</p>
        <p>Zack put a post up on Facebook about his growth plan and the direction of his life that resonated with a lot of his friends. Anand read this post, and particularly resonated with the part about almost being homeless in Vegas. Funny enough, Anand had a similar story. Anand reached out to Zack after reading that post, with literally perfect timing. They finally got on a call as Zack was about to go to work, shared their stories and their visions of the future, and finally decided they'd be working with each other. Zack didn't go back to his job at Peppermill, and didn't go back after that. The weird thing about working at restaurants is that for some reason after you quit working at them the management is typically a lot friendlier. You'd think if it was the opposite situation there wouldn't be such a huge turnover rate.</p>
        <p>Initially, Anand put Zack through sort of a "Hell Week" while trying to sort out a Facebook ad account. It was a week of staying up until morning doing Facebook Ads trainings with Anand while blasting "The Final Countdown" when he and Anand became quite mentally retarded from staying up so late, (Zack was already used to graveyard shift, only this graveyard shift was in the comfort of his home.), drinking energy drinks, eating <a href="https://web.archive.org/web/20201022150258/http://www.desiburrito.com/">Desi Burrito</a> (sadly, they're closed now. This was Zack's literal favorite restaurant in Vegas), and at one point almost having a caffeine overdose from drinking two Monster energy coffee drinks (Don't do this. Ever.). This was an unpaid week to test Zack's grit, and luckily before he started Zack saved an extra $500 to go this week without pay (literally the perfect amount), and afterwards he was paid a solid $500 a week.</p>
        <p>After that initial week, Zack became a part of the team. Zack, Anand, and a few other team members were in super startup mode, something Zack knew next to nothing about even though he did read a lot of business books at this point, he couldn't really grasp the concept of business at the time. Zack was particularly gifted at copywriting. So much so that one of his Ad Copy mixed with Anand's Facebook Ads expertise lead them to hitting $20,000K daily revenue for their client making them a literal millionaire. That client was super paranoid and ended up blocking us and caused massive damages to the agency, but we still kept going.</p>
        <h3>2018</h3>
        <p>A couple of months past, and Anand decided it would be a good idea to invest in Zack, and he chose the perfect person to do it. His name was Ryan Donaldson.</p>
        <p>To Zack, Ryan was a new level of person that Zack had only speculated existed. Anand was already an extraordinary person, but to Zack, Ryan was on a new level. His communication skills and logic blew both Zack and Anand's minds. For a while we were both getting mentoring from him. Ryan was a business genius who was really good at sales and worked behind the scenes on a lot of popular business projects. He took a liking to Zack, and trained him in the areas of business strategy, logic, commuincation skills, and even how to talk to girls properly. This was really effeting Zack at the time, and Zack had a lot of unlearning he had to do from learning "Pickup" from weird men on Youtube for so long. Ryan's level of charisma and understanding of how to navigate social situaitons was like nothing Zack's ever seen before. Also, Zack's sex life and communication skills got REALLY good after his coaching calls with Ryan.</p>
        <p>During the next year, the team decided to all meetup in Colorado to mastermind and build a startup. Eventually most of the team would move there, Zack &amp; Anand certainly did, and some of our team was already there. Initially, the company was paying for Zack to stay at a hotel. This was the first time Zack met Anand in person since New Orleans. Ryan Donaldson actually flew out there too and it was a really productive time.</p>
        <p>Now for another funny startup situation. The startup we built totally failed. Not because we didn't sell enough products, but because we oversold, and we did so at a huge amount. This wasn't because they were scammers or anything had any bad intentions. It was because incompetence. They had zero experience in building a manufacturing company, nor how to build a team to manage it without them. They were good at was building Ecommerce stores online and selling products online. Initially Zack thought it was a weird idea not to just hire other businesses to do dropshipping for us, but Anand was deadset on doing everything on our own. This was one of the biggest literal million dollar fuckups that Anand had ever had, and Zack got to witness. This was actually really useful learning for Zack.</p>
        <p>At this point, things weren't looking so good. The marketing agency was pretty much dead already, the Ecom store we made was on fire and was burning in business hell (Zack didn't realize that was possible until people charged back after they already spent their money on paying the team that didn't deliver. They even stopped paying that and we still didn't have money. Zack also lost his ability to use Paypal because it was tied to that store. That's why you'll never see any options to pay with Paypal from Zack 😉), and Anand still had backup plans upon backup plans on how to recover. Because of Zack's loyalty and friendship with Anand, Zack was still part of those plans.</p>
        <p>Before everything went to total shit, Anand was invited by the owners of a Ukrainian AI Facebook ads management software to visit Ukraine. Anand left for about a month whlie most of the team was still in Colorado, and discovered a ton about their culture and fell in love with the country &amp; the people within it. When he came back, Anand told Zack about everything there and shared his enthusiasm, and Zack picked up on it. He also met the most beautiful, brilliant woman who would eventually become a project manager for the new Ukrainian team we were going to build, and her name was Olga.</p>
        <p>Olga had her own team of Ukrainians she would be managing. While Anand and I were still in the states, Olga was in Ukraine managing her team to support us on our projects.</p>
        <p>Just to reiterate, we were amazing at Ecommerce web design and marketing. The reason everything at this point was failing was because there was too much debt and legal attacks coming towards the agency from every direction that it was super stressful and pretty hard for the remaining team (the few of us who didn't quit) pretty much to breathe. Then, the new plan.</p>
        <p>Anand was the business mastermind at the time, while Zack was a really strong communicator, process creator, and general strategy creator at this time thanks to Ryan's trainings.</p>
        <p>
          By the way, pretty big but important side note: Zack concluded his trainings with Ryan towards the end of this year, not because the company was failing or he felt Ryan was a bad teacher, but because Ryan gave Zack so much value that Zack just felt good about moving forward with his life on his own. He was mentally able to be mentally self-reliant, and thanks to a lot of Ryan's mental frameworks, critical thinking mehtods, and other things Zack learned during their coaching sessions, Zack knew what he needed to get to where he wanted to be, and Ryan trained him enough. On one of the last lessons, because of how Zack's unique mind worked, Ryan suggested that Zack learn the programming language of Python. Initially this was so Zack could learn about stocks by creating a stock simulator, but Zack found it to be more valuable and interesting than that. Either way, Ryan's suggestion was spot on and Zack really fell in love with programming and wanted to focus on building his skillset in software development. This is importnat to know for later, and as you can see from this website, he got pretty good. Good enough at least 🙂. Now back to the story.
        </p>
        <p>Anand created a plan to rebuild from scratch everything. The team, our bank accounts, everything. And based off of his research in Ukraine, he decided that the best course of action. Anand and Zack were going to go to Ukraine to build and train the Ukrainian team along side Olga.</p>
        <p>Anand went to Ukraine first as he was the leader of the company (when I say company, that really means just different names and legal structures around Anand) and there wasn't much liquidity available. At this time, Zack went back home to Mississippi for about a month until the team was able to pay for him to come back out.</p>
        <p>During this month, there were a few things going on.</p>
        <ol>
          <li>Zack remembered exactly why he left Mississippi in the first place.</li>
          <li>He spent a lot of time with his old friends.</li>
        </ol>
        <p>And 3., Olga and Zack were messaging each other... a lot. Sometimes about work, sometimes about life and each other, whatever was really there at the time. Both of them were super happy to recieve messages from one another, and talking to each other was always so interesting and natural. Zack didn't know what they were going to be, but he knew they were going to be close.</p>
        <p>The end of this month was also hell, mostly because Mississippi is pretty boring and people get sick there all the time because about 95% of people don't take care of their health, and they're really not the smartest.</p>
        <p>Mississippi is literally #1 in two things:</p>
        <ol>
          <li>Obesity</li>
          <li>Poverty</li>
        </ol>
        <p>Zack knew both of these things, and while he was smarter and a completely transformed and different person from the point when he left here in 2016, for the most part, Mississippi stayed exactly the same.</p>
        <h3>2019</h3>
        <p>One night, Zack recieved a call from Anand, and it was the best call he could've recieved. "Hey buddy, so Olga and I were crunching the numbers we have some good news: Pack your bags buddy because you're coming to Ukraine." To Zack, the feeling he experienced was what he'd imagined it felt like for the contestents on American Idol to hear "You're going to Hollywood!". Again, Zack said his goodbyes, and he left.</p>
        <p>Upon Zack's arrival to Ukraine, Anand had met him on the airport, and soon after, Anand said "Turn around" and Zack saw Olga with a huge smile on her face. Zack said "HOLY SHIT!" out of surprise, gave her a huge hug and physically picked her up and spun her around out of excitement. From day 1, moment 1, Zack &amp; Olga came together like magnets, and it never really stopped.</p>
        <p>During Zack's first week in Kyiv, Ukraine, besides work and time at the office, Olga took care of Zack and showed him around the city. This was a huge benefit to Zack because he spoke minimal amounts of Russian and it was pretty easy for him to get lost. About 10 days after arriving, they had the most magical night together and shared their first kiss.</p>
        <p>The newly developed company that Anand created and Olga was a partner in had a lot of ups and downs. Some weeks there would be pay, other weeks there weren't. We had to get creative with how we were going to pay the Ukrainion team since we had a difficult time getting the international payment system Payoneer setup. Ultimately, the company was failing. Olga and I were also falling in love and decided to be in a relationship together, which was probably the main thing that kept me grounded at the time.</p>
        <p>A standard Visa for an American going to Ukraine only lasts 90 days, so if you're travelling to Europe and don't get a work or education visa, or aren't married to someone from the country, you have to leave the country before that time is up. Otherwise, you may get banned from the country. After 180 days however, your Visa resets and you can re-enter the country like normal.</p>
        <p>Anand's visa expired first, so he left to the nearby country of Moldova about a month and a half after Zack's arrival to Ukraine. Olga is one of the partners in the new company, along with Anand and one other member, so it would've made sense for her to go then. She decided to stay with Zack in Kyiv, and when it was his time to leave, we both travelled to Moldova.</p>
        <p>Moldova was a hell hole, actually not to dissimilar from Mississippi. If you imagine a post apocolyptic city filled with Zombies, but instead of zombies there were just normal citizens, that's Moldova. During the time Zack &amp; Olga had a lot of challenges in the relationship and with work. It was Zack's first experience living with a woman, his second experience living in new country where he now knew even less of the language than he did in Ukraine, and this country happened to be Moldova. Olga had to go back to Kyiv to handle some business tasks along with Anand, so she left and was coming back in a month.</p>
        <p>Zack was severely stressed and depressed at the time she left. Zack &amp; Olga were still a couple, but Zack hit a new, different form of depression about a week or 2 before Olga's departure. There's a phenomonon in the mind Anand told me about called a "Terror Barrier" that a lot of people reaching for success go experience. This process is occurs when there are 2 versions of you:</p>
        <ol>
          <li>There's the old you, with the old patterns and belief systems that were working for a time, but only got you so far</li>
          <li>Then there's the new you: The version of yourself you're wanting to evolve into.</li>
        </ol>
        <p>Only one of these versions, and as their own live entities, will survive, and until that happens there's a pretty gnarly period of inner turmoil and existential criseses that can occur. In this case, the old Zack had to die in order to accept and thrive in his new life.</p>
        <p>In the month that Olga was gone, Zack had gotten to the point of stress that he'd never experienced before. Luckily, this wasn't Zack's first experience with depression, and it also wasn't his first time dealing with insomnia and anxiety that came along with it. This month was hard, mentally painful, and, well, groundbreaking. Every single day Zack was working out, taking care of his body, taking supplements, and eating as well as he could. At one point, in one of his worst days, he snapped. The morning started with him going to exercise and meditate in a forest as he'd been doing for a couple of weeks now, and something wasn't right. His thoughts were so loud, so intrusive, and they wouldn't stop even a little. They exhausted Zack so much that he stopped, sat on a park bench, and did nothing. He closed his eyes, crossed his legs, and was just breathing.</p>
        <p>It was as if all of the lessons from the past year, learning from Ryan, Anand, Anand's Mentor Travis, and all of any business experience Zack picked up along the way just flashed back in his head. Then, the thoughts calmed down, and his head cleared, and Zack had an identity shift. He walked into the woods that morning as Zack the employee and transformed into Zack the CEO. There's really no other way to explain it other than that. Zack loved Olga so much that he had to figure out his life together otherwise he was pretty sure it wasn't going to work. From there, all of that stress turned him into a diamond. His brain was hungry for knowledge, he was resourceful, he did about 2 weeks of non-stop research in freelancing and relationships to get himself to a point where he could build his own independent income and thrive in his new relationship.</p>
        <p>Olga came back, and she noticed that progress that was made. It still wasn't easy at first, but overtime, Zack had his new freelancing business earning enough money for him and Olga to survive on his income, and the relationship went from failling to thriving.</p>
        <p>And that pretty much brings us to now 🙂.</p>
        <h3>2020 - Present</h3>
        <p>I'll go ahead and talk in the first person now. I've lived a really amazing life so far, and as I write this story, I'm 22 years old and still only just getting started. I've never wrote this out so in depth, and still I feel I left a lot out, but definitely got the important parts.
        </p>
        <p>My goal with building this website is to share my talents, services, perspective, advice, anything I have to offer of values to people so that we may work together to leave a massive positive impact on the world.</p>
        <p>I hope you'll join me, either directly or indirectly, to make this world a better place.</p>
        <p>If you're interested in working with me or would like to get in touch, the best way to contact me is to either message me through my <a href="https://web.archive.org/web/20201022150258/https://facebook.com/zackplauche/">Facebook page</a> or to email me at <a href="https://web.archive.org/web/20201022150258/mailto:zackknowspython@gmail.com">zackknowspython@gmail.com</a>.</p>
        <p>Thank you for reading. 🙂</p>
      </section>
    </section>
  </div>
</template>

<script setup lang="ts">

const values: Value[] = [
  {
    emoji: '🤩',
    topValue: true,
    name: 'Maximum Fun',
    description: 'Fun = Sustainable. Do awesome things on your own and with people you love. Every other value is just a way to maximize fun.'
  },
  {
    emoji: '💎',
    name: 'Clarity',
    description: 'Good decisions come from a foundation of truth. Hard whole truths are greater than pleasant lies. Analytics is Digital Awareness.',
    topValue: true,
  },
  {
    emoji: '🥩',
    name: 'Super Healthy',
    description: 'Energy, mental clarity, being strong, and being a BEAST ftw 🔥 The world needs good, strong people now more than ever.',
    topValue: true,
  },
  {
    emoji: '✅',
    name: 'Outsized Results',
    description: 'I aim to produce and provide outsized returns for myself and others, and learn from outliers.',
    topValue: true,
  },
  {
    emoji: '💪',
    name: 'Play to Strengths',
    description: 'Do what you love doing and outsource the rest as much as possible.',
    secretDescription: 'The world needs more good and strong people.',
    teamValue: true,
    coreTenant: true,
    topValue: true,
  },
  {
    emoji: '🌿',
    name: 'Nature',
    description: 'Spending time in nature can bring a feeling of presence, calmness, creativity, connectedness, and peace of mind.'
  },
  {
    emoji: '⌚',
    name: 'Punctuality',
    description: 'I value and respect my own time highly, and so to the time of others.'
  },
  {
    emoji: '🌀',
    name: 'Oneness',
    description: 'Everything is connected. Take a holistic view and see the big picture. Life and business are not separate.',
    topValue: true,
  },
  {
    emoji: '🌱',
    name: 'Seed Planting',
    secretName: 'Take Care of Your Plants',
    description: 'Rome wasn\'t built in a day. Plant seeds and water them daily so you can enjoy orchards in the future.',
    oldDescription: 'Think long-term, take small actions today that\'ll lead to the results you\'ll want in the future.',
    // topValue: true,
  },
  {
    emoji: '🌳',
    name: 'Patience',
    description: 'Cause and Effect. Employ patience to work hard and enjoy the fruits of your labor when you\'re actually winning.',
  },
  {
    emoji: '💪',
    name: 'Strength',
    description: 'Be strong to protect others. And because it\'s fun and looks awesome haha.',
    topValue: true,
  },
  {
    emoji: '🔁',
    name: 'Consistency',
    description: 'Making small beneficial actions overtime produces massive reults.',
  },
  {
    emoji: '💠',
    name: 'Growth',
    secretName: 'Growth & Improvement',
    description: 'Consistent focused high-volume of hard-work overtime produces results. Build quality, and build to completion.',
    // topValue: true,
  },
  {
    emoji: '💠',
    name: 'Growth',
    secretName: 'Growth & Improvement',
    description: 'Consistent focused high-volume of hard-work overtime produces results. Build quality, and build to completion.',
    // topValue: true,
  },
  {
    emoji: '🧘‍♂️',
    name: 'Presence',
    description: 'Being in your body and connecting to your environment helps you feel good and enjoy life more, and enjoying life is fun.'
  },
  {
    emoji: '️️⚫',
    name: 'Simplicity',
    secretName: 'Process Maps & Automation',
    secretName2: 'Processes & Automation',
    coreTenantName: 'A Process Map For Everything',
    description: 'It doesn\'t have to be easy, but keeping things clean, neat, and simple helps others understand easier which creates speed.'
  },
  {
    emoji: '️⚙️',
    name: 'Automation',
    secretName: 'Process Maps & Automation',
    secretName2: 'Processes & Automation',
    coreTenantName: 'A Process Map For Everything',
    description: 'A process map for everything. Nothing like labor that doesn\'t need days off, saves time, and produces results.',
    secretDescription: 'Map out business processes and automate the business processes that have been mapped out!',
  },
]


const topValues = values.filter(value => value.topValue)

useHead({ title: 'About ' })

interface Value {
  emoji: string
  name: string
  description: string

  // Optional Properties
  oldDescription?: string
  topValue?: boolean
  secretDescription?: string
  secretName?: string
  secretName2?: string
  coreTenant?: boolean
  coreTenantName?: string
  teamValue?: boolean
}


</script>

<style scoped>

h2 {
  @apply text-7xl font-serif text-blue-dark font-normal;
}

</style>