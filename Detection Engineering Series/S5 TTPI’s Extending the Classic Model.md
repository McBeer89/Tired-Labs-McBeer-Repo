# TTPI's: Extending the Classic Model

**Author:** VanVleet  
**Part of:** [Threat Detection Engineering: The Series](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62)

![VanVleet Profile](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

---

In 1926, Erwin Schrödinger introduced a new model of an atom. The previous "planetary" model, created by Niels Bohr in 1913, theorized that electrons moved around the nucleus in orbits of fixed size and energy. Schrödinger offered a more precise description of the movement of electrons, allowing it to model complex atoms that Bohr's model could not. Schrödinger's model became the foundation of modern quantum mechanics and is still widely accepted as the most accurate atomic model available. [Atomic Models — Compound Interest]

Models help us simplify, analyze, and explain complex real-life concepts. They are used everywhere and have been fundamental in enabling major advancements in our understanding of the world. But sometimes, models become an obstacle to advancement because they are too simple and limit our ability to account for the complexity of the thing they model.

In the InfoSec industry, we have some well-known models that help us to simplify, categorize, and analyze attacker behaviors. These include the taxonomy of "Tactics, Techniques, and Procedures (TTPs)" and David Bianco's ubiquitous "Pyramid of Pain." Like Bohr's atomic model, these models have enabled improvements in how we identify, categorize, and communicate attacker tradecraft. But, also like Bohr's model, they simplify too much and have become an obstacle to further progress. It's time for more precise models.

## Tactics, Techniques, and Fuzzy Procedures

Much ink has been spilt on defining TTPs. If you're unsure what they are, Robby Winchester wrote an excellent article that harks back to the DoD definitions, which is where the concept originated.

I think everyone is pretty clear on tactics and techniques, so I'm going to use simple definitions:

**Tactic** — A high-level grouping of actions that provide a specific benefit to an attacker.

**Technique** — A general method for achieving a tactic.

Note that both tactics and techniques are abstract concepts: high-level, without any specific implementation details. They are extremely useful for categorization and analysis, but you can't do or detect a tactic or technique. Nothing is concrete until you reach the procedure level.

Procedures are where the concept gets fuzzy, and that's because they do all the work that happens below "technique." All of the real-world usage of attacker tradecraft is encompassed in the P in TTP. In an article titled "What is a Procedure?," Jared Atkinson points out that attacker tradecraft can be described in at least six layers of abstraction, yet the TTP taxonomy offers only three. And all of the compression happens at the Procedure layer. In the TTP model, Procedure is doing a lot of heavy lifting!

## What IS a Procedure?

So, what IS a procedure? Going back to Robby's article, the DoD describes them as "standard, detailed steps that prescribe how to perform specific tasks." Jared offers an excellent clarification: "The procedures are the pattern of steps to execute, not the execution of the steps." He gives this example of a procedure for the technique of dumping credential from lsass.exe:

1. Determine the process identifier for lsass.exe.
2. Open a handle to lsass.exe with at least the PROCESS_VM_READ access right.
3. Read the memory of lsass.exe.

The procedure is the recipe for a specific method of dumping lsass.exe to obtain credentials. Running with this cooking metaphor, the procedure is the recipe, not the cake that it produces. And there might be other recipes that do it differently but produce the same kind of cake; these represent other procedures.

I am an adherent of Jared's definition of procedure, but in discussions with colleagues throughout the industry, I've realized that other interpretations of the term are in use and, under the current TTP model, are equally valid. For example, MITRE's ATT&CK framework lists "Procedure Examples" for each technique, all of which are a single, specific instance of attackers or tools using the technique. In other words, it's a list of cakes, not recipes. (In fact, there IS no list of recipes for any given technique currently in existence. That's one goal of the TRR Library). Shortly after embarking on a discussion of detection engineering with a new colleague, I find myself needing to clarify which definition of 'procedure' they are using: recipes, cakes, or a combination of both?

I believe that a big part of this problem is that our current model is too simple. The TTP taxonomy stuffs both cakes and recipes into a single layer. No wonder we find ourselves struggling to distinguish between them!

## TTPI — Adding the Instance Layer

To address this problem, I propose extending the TTP taxonomy to include a new "Instance" layer. This new layer separates recipes from cakes:

**Tactic** — The goal an attacker wants to achieve. (Feeding people)

**Technique** — A general method for achieving a tactic. (Baking a cake)

**Procedure** — A unique pattern of detailed steps to accomplish a technique. (The cake recipe)

**Instance** — A concrete implementation of a procedure. (The cake)

To illustrate this new taxonomy, I'm going to break down the technique for clearing Windows event logs (T1070.001). (I'm going to assume a lot of knowledge about this technique, if you need more background please see the TRR on it.)

### Clear Windows Event Logs (T1070.001)

**Tactic:** Defense Evasion

**Technique:** Clear Windows Event Logs

**Procedures:**

- An attacker can clear event logs using the MS-EVEN or MS-EVEN6 RPC methods.
- An attacker can clear event logs by redirecting them to attacker-controlled files via the registry.
- An attacker can clear event logs by killing the EventLog service and deleting the log files.

**Instances:**

- Executing 'wevtutil cl system' at the command line.
- Using the PowerShell 'Clear-EventLog' cmdlet at the command line.
- Using the PowerShell 'Clear-EventLog' cmdlet in a script that is downloaded from an Amazon S3 bucket and executed via the 'iex' cmdlet alias.
- Calling the EvtClearLog() Windows API in a binary named 'erase.exe.'
- Running a VB script in an Office document macro that calls WMI's ClearEventlog() method.
- Running a script named 'foo.ps1' to terminate the svchost process hosting the EventLog service and delete all files in '%SystemRoot%\System32\winevt\Logs\*.evtx.'
- …. (MITRE lists 41 instances, and that's just the tip of the iceberg)

## Of the Finite and the Infinite

The TTPI model yields some immediate benefits by allowing us to distinguish procedures from instances. One thing that becomes immediately clear is that procedures (again, the recipes) are finite. There are only so many ways to get the operating system to do something specific.

Procedures do change, but at a slow rate. Updates to operating systems and platforms render old procedures inoperable (Credential Guard killing LSASS dumping, for example), while new platforms or technologies introduce new ones (AI conveniently collecting and serving up Credentials from Password Stores [T1555], for example).

Instances, on the other hand, are categorically infinite and can change rapidly. Adversaries have moved to living-off-the-land, lighter weight tools and scripts, and malware-as-a-service to constantly refresh their instances and stay ahead of instance-focused detections and signatures. And the era of GenAI will make that even easier.

One other observation is that very instance maps to a single procedure, and many instances can implement the same procedure. For example, the wevutil.exe utility, PowerShell's Clear-EventLog cmdlet, and WMI's ClearEventLog() method are all different instances, but they all implement the exact same procedure: they call one of the MS-EVEN or MS-EVEN6 RPCs.

So, procedures are finite and slow to change, instances are infinite and fast changing, and all instances employ one procedure. Hold that thought.

## Revisiting the Pyramid of Pain

Let's take our new TTPI taxonomy and use it to refine David Bianco's "Pyramid of Pain."

<!-- Image: Original Pyramid of Pain diagram by David Bianco -->

The pinnacle of the pyramid is "TTPs." David explained this level by saying "When you detect and respond at this level, you are operating directly on adversary behaviors, not against their tools." The detection engineers I've talked with universally agree that the ideal is to detect these "TTPs" at the top of the pyramid.

The challenge is that tactics and techniques are abstract and undetectable, and procedures (the 'TTP' version) encompass both recipes and cakes. That leaves a lot of gray area: detecting both recipes and cakes can be considered detecting "TTPs".

We see this confusion in the many public detection repositories: detections for both recipes and cakes abound (the latter being more abundant than the former, in the author's opinion).

I'd like to offer a refined pyramid, which I'm going to call the **Pyramid of Permanence**.

<!-- Image: Pyramid of Permanence diagram - refined version with TTPI taxonomy -->

This pyramid stacks elements by ease of modification or replacement, just like Bianco's pyramid of pain, but our new TTPI taxonomy allows us to greatly simplify it: Procedures (using the TTPI definition) are the pinnacle. Everything below that is just an element of an Instance.

When it comes to detecting attacker tradecraft, we still focus on the pinnacle. When you take an instance away from an attacker, they just create a new one. But when you take away a procedure, they can't just create a new one. They have to operate in a smaller space.

MITRE's Summiting the Pyramid defines levels of analytic robustness for scoring a given detection that align neatly with this pyramid model. Levels 4 and 5 define detections that are focused on procedures, while levels 1–3 focus on instances. (Side note: whether a detection can reach level 5 will often come down to how different the procedures are. For cases where the procedures are drastically different, like credentials from the NTDS.dit, multiple level 4 detections are the highest you can achieve, and together they would comprise a level 5 detection strategy.)

## Don't Chase Instances

The new models help clarify a valuable lesson: don't chase instances. Instances are infinite. Attackers are constantly making new ones, and no matter how fast we move, we'll always be chasing: them deciding where to go next and us having to follow along. You can't get ahead in an infinite space.

This doesn't mean there is no value in detecting instances. Low cost, high fidelity detections for commonly-used instances are absolutely worthwhile. There is definitely value in identifying and responding to oft-abused tools like CobaltStrike and Rubeus, for example.

But, the most impact is gained by denying procedures. Returning to that earlier thought: procedures are finite and slow to change, instances are infinite and fast changing, and all instances employ one procedure. Attackers must use procedures, yet there is a finite number of them. If we focus on detecting them directly, we detect all instances that use the procedure and force the attacker to abandon it or get caught. That's a game we can win.

## Conclusion

New models can facilitate new understanding. By extending the TTP and Pyramid of Pain models, we can more clearly target our detection engineering efforts where they'll provide the most impact. Share your thoughts in the comments, and if you agree share the article with your colleagues. Let's get clarity between those recipes and cakes!

---

**Tags:** Threat Detection, Detection Engineering, TTPs, MITRE ATT&CK