# Improving Threat Identification with Detection Modeling

**Author:** VanVleet  
**Published:** February 26, 2024  
**Reading Time:** 13 min read  
**Part of:** [Threat Detection Engineering: The Series](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62)

![VanVleet Profile](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

---

<!-- Image: Article header image - not accessible -->

This article is part of a [series on Threat Detection](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62). In this post, I'll present a simple approach to detection modeling and demonstrate how a Detection Data Model (DDM) they can be used as an analytic technique to help with the task of identification.

In this article I'm building on previous topics, so you'll find it easier to follow along if you've already read my articles on [Identifying and Classifying Techniques](https://medium.com/@vanvleet/identifying-and-classifying-attack-techniques-002c0c4cd595) and overall [Threat Detection strategy.](https://medium.com/@vanvleet/threat-detection-strategy-a-visual-model-b8f4fa518441)

## Structured Analytic Techniques: What and Why?

Let's start with a story.

In March 2023, CVE-2023–23397 was released. The vulnerability involved sending an Outlook calendar invite with the *PidLidReminderFileParameter* set to an attacker-hosted external file. This caused Windows to attempt to authenticate to the external share with the NTLM password hash, exposing the user's hash. Crowdstrike quickly responded by publishing a [hunting query](https://www.reddit.com/r/crowdstrike/comments/11sda83/situational_awareness_hunting_microsoft_outlook/) to find the activity.

Except… the published query didn't actually detect the attack technique. The query was looking for outlook.exe making outbound SMB connections, but it was the SYSTEM process (PID 4) that makes the outbound SMB connection. The detection had excellent theoretical classification (outlook.exe really shouldn't be making outbound SMB connections) but achieved 0% identification, resulting in a 0% probability of finding the technique.

So what went wrong? Crowdstrike's analyst didn't fully understand how the technique worked (none of us did because it was new!) and he made a reasonable but incorrect assumption. Now, please don't misunderstand. The purpose of this story is not to insult the excellent work that Crowdstrike — and the particular analyst who made the post — does to help us all keep our networks safe. **The purpose of this story is to demonstrate that even the most experienced detection engineers can make identification mistakes that sabotage their threat detection efforts.** These mistakes happen because attack techniques are abusing complex technical systems. When dealing with complex information, the human mind is excellent at making assumptions to fill in gaps.

In the world of intelligence analysis (where I started my career), analysts are taught to use [structured analytic techniques](https://www.cia.gov/static/Tradecraft-Primer-apr09.pdf) to make their analysis resistant to mental mistakes. These techniques help reveal where our information or understanding is incomplete and we're making assumptions to fill in gaps. Once we can identify our knowledge gaps, we know what details we need to find for a more accurate understanding. Even if we can't fill those gaps, we can at least be deliberate and explicit about the assumptions behind our thinking.

Returning to the world of detection engineering, identification is a difficult task fraught with possible mistakes about complex technical details. It is further complicated by limited visibility into those systems. In order to help us accurately understand an attack technique and determine the best way to identify it, we can employ a structured analytic technique: a detection data model.

## Detection Data Models

**A detection data model (DDM) is an analytic tool that facilitates the process of modeling an attack technique, i.e. mapping out the operations required to implement an attack technique and uncovering any gaps in your understanding of that technique.** It also maps in potential telemetry sources to assist with finding the best available approach to identifying an attack technique. To borrow a term from Jared Atkinson, the DDM helps you [find the base condition(s)](https://posts.specterops.io/thoughts-on-detection-3c5cab66f511) for an attack technique (definitely recommend reading his post!)

I'm honestly not sure who first came up with the term "detection data model," but there is a great deal of prior work on mapping out attack techniques. Jose Luis Rodriguez and Roberto Rodriguez have [done](https://posts.specterops.io/defining-attack-data-sources-part-i-4c39e581454f) a [great](https://www.youtube.com/watch?v=eM0c_Gil-38) [deal](https://www.youtube.com/watch?v=QCDBjFJ_C3g) with detection models in the [OSSEM project](https://ossemproject.com/dm/intro.html). Jared Atkinson has an excellent [series](https://posts.specterops.io/understanding-the-function-call-stack-f08b5341efa4) that demonstrates how to map Windows techniques via '[operation graphs](https://posts.specterops.io/on-detection-tactical-to-functional-a3a0a5c4d566)' and previously worked on mapping via '[capability abstractions](https://posts.specterops.io/capability-abstraction-fbeaeeb26384).' I have borrowed elements from each of these modeling approaches in crafting my version of a DDM.

My goal was to create a detection model and process that would be lightweight and flexible enough to map any attack technique on any platform (various OSes, network, cloud, etc). **Keep in mind that this is an analytic technique: there is no single correct model.**

The purpose of a detection data model is to:

1. Map out the **specific**, **essential**, **immutable**, and theoretically **observable** elements of an attack technique to ensure you have a detailed and complete understanding of how it works. (And to make sure you're "[playing with a full deck](https://posts.specterops.io/thoughts-on-detection-3c5cab66f511)!")
2. Distinguish between unique procedures that implement the same technique.
3. Find potential telemetry to identify the technique with the highest possible confidence.

Here is an example of an incomplete DDM for the attack technique identified in CVE-2023–23397. (I'll talk later about why I left it incomplete.) Following the style of Jared's operation graphs, I use a circle to represent each 'operation' that takes place. Arrows indicate the flow of operations, and labels and tags are used to include potential telemetry sources and important details like processes, APIs, filenames, etc.

<!-- Image: DDM diagram for CVE-2023-23397 showing operations with a question mark indicating incomplete understanding -->

## Creating a DDM, Step by Step

Now that we've talked about why to use a DDM and given an initial example, let's walk through the process of creating a DDM. I'm going to use the technique "[Create or Modify System Process: Windows Service](https://attack.mitre.org/techniques/T1543/003/)" (T1543.003) as my example here. I'll specifically focus on creating a remote service, so I can demonstrate how to map out a procedure that involves two machines. I use the [Arrows](https://arrows.app/) app in this demo, but any drawing application works.

> Please note: I am not going to go into how to deep dive into a technique here because my focus is on mapping the technique, not analyzing it. Trying to do both would make a VERY long post. Jared's posts cited above (and more articles [here](https://posts.specterops.io/understanding-the-function-call-stack-f08b5341efa4) and [here](https://specterops.io/wp-content/uploads/sites/3/2022/06/RPC_for_Detection_Engineers.pdf)) walk through a lot of that process for various techniques. They would be an excellent place to start if you need to learn those skills.

The first step is to map out your understanding of the technique as best you can. Try to define operations that are as granular and specific as possible, but it's not critical to get it right initially. We'll iteratively work to expand operations. A few principles to keep in mind:

* Each operation will be a circle and should use an "Action Object" pattern for naming.
* Use arrows to indicate the progression from operation to operation
* If the procedure involves two machines, make operations on the source machine a green circle and the target machine blue.

So, here is my first attempt at mapping out the operations in creating a remote service, just based on some initial googling.

<!-- Image: Initial DDM showing "Open SCM" (green) → "Call CreateServiceW" (green) → "magic happens" → "Create Registry Key" (blue) -->

First you have to open a handle to the Service Control Manager on the target machine, and then you call CreateServiceW with the details of the service you want created. Then magic happens, and on the remote machine a registry key is created.

Then you ask some questions about each operation you've mapped:

* Do I understand what's happening here? Do I know what processes, APIs, network connections, and securable objects are involved in each step? Is it clear how one operation causes or is followed by the next operation?
* Is this a specific, granular operation or a summary of multiple other operations? Is this the [right level of abstraction](https://posts.specterops.io/capability-abstraction-fbeaeeb26384), or do I need to delve lower?
* Is this operation essential to accomplishing the technique? If an operation is optional (like unmapping the existing section in Process Hollowing) then it should **not** be included on the DDM. This will make more sense when we talk about how to use it.

For the Open SCM operation, I have to admit that I know almost nothing of what's involved there, so that's the first place to go deeper. A review of the documentation for [CreateServiceW](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-createservicew) refers me to the API [OpenSCManager](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-openscmanagera) for this step. I can see that "opening SCM" means I need to call this API, so I'm going to rename this step "Call OpenSCManager." Other than that, this operation seems pretty specific and straight-forward: I call it, provide the remote machine I want, and I get back a handle that I can use with CreateService. So, I'm happy with where this is at and feel comfortable that I understand this operation.

The next operation is "Call CreateServiceW." The relationship between this operation and the one that follows it is not clear: my best description of the next step is "magic happens and a remote key is created." Clearly there is a lot I don't understand here. For example, how is the remote machine being informed that it needs to create a registry key? What process is doing that? As mentioned, I'm going to skip over the technical analysis right now, but at this point you'd go and do that research and discover that CreateServiceW calls a Remote Procedure Call (RPC) named "[RCreateServiceW](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-scmr/6a8ca926-9477-4dd4-b766-692fab07227e)" on the target machine. This RPC service is hosted in the Windows binary services.exe. Let's add that to our DDM. We use a downward arrow to indicate that the operation below is part of the implementation of the operation above, not a new step. In other words, it's a lower layer of abstraction. For "Receive RPC" we're using an upward arrow to show that the "Create Registry Key" operation is completed by the RPC code on the target machine (you can see this by looking at the implementation of RCreateServiceW in your favorite disassembler).

<!-- Image: Refined DDM showing "Call OpenSCManager" → "Call API" (with tag: API: CreateServiceW, Process: any) → downward arrow to "Call RPC" (RPC: RCreateServiceW) → "Receive RPC" (Process: services.exe) → upward arrow to "Create Registry Key" -->

We want to keep the operations granular but general, so at this point I'm also going to change the "Call CreateServiceW" operation to "Call API" and added a tag to note the specific API that's being called. I've also added in a tag for the process responsible for each operation. You'll use tags for any specific details, like file names, registry keys, network ports or protocols, API calls, etc. Make sure you only include the essential and immutable details: if you have an operation of "Write File" and the attacker can choose the filename, tag it "File: any" or don't tag it at all.

Now we go through the iterative process and ask the same questions of our new operations. In this case, I still don't know the specifics of how this data is transiting the network. "Remote Procedure Call" is a known entity, yes, but each RPC can use different network transports. This tells me that I need to delve deeper to understand what's happening during this operation. Skipping the technical details (but you can read about them [here](https://specterops.io/wp-content/uploads/sites/3/2022/06/RPC_for_Detection_Engineers.pdf)), we learn that the [Service Control Manager Remote Protocol [MS-SCMR]](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-scmr/705b624a-13de-43cc-b8a2-99573da3635f) has [two possible network transports](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-scmr/4c8b7701-b043-400c-9350-dc29cfaa5e7a): SMB using the named piped "\PIPE\svcctl" or TCP. Let's add these to our map.

<!-- Image: Further refined DDM showing "Call RPC" branching downward to two options: "Connect SMB" (Pipe: \PIPE\svcctl, Process: ?) and "Connect TCP" (Port: 49152-65535, Process: ?) -->

I don't actually know which process would make these TCP or SMB connections, so I'm tagging them with "Process: ?" Again, I used a downward arrow from "Call RPC" to the new operations, because they are a lower abstraction layer: they are how the "Call RPC" operation is implemented.

Going through the iterative process again, I'm now feeling like I have a pretty solid understanding of how this technique works. Each operation is granular and specific, in that it doesn't appear to summarize multiple operations. At this point, I feel like I have a solid understanding of the operations required to implement this technique.

Now it's time to add in the telemetry for each operation. If you're not certain that a source will record the operation, add it and then you can test it out later. In this use case, I know that [Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) event 18 records connections to named pipe, so that might be an option. I also could potentially see network traffic in firewall logs or with network sensors. Creating a new service can generate events 4697 and 7045, and analysis of the code for RCreateServiceW (in our "Receive RPC" operation) shows that they are generated there, so we'll add those to that operation. And Sysmon 12 records the creation and deletion of registry keys, so I'll add that. Finally, if I can [set a SACL](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/registry-global-object-access-auditing) on the [SCM database in the registry](https://learn.microsoft.com/en-us/windows/win32/services/database-of-installed-services), event 4663 would notify me of changes. You should also add in any telemetry your EDR or other security solutions might provide. Here's our DDM with telemetry sources:

<!-- Image: Complete DDM with telemetry annotations on each operation showing available log sources like Sysmon 18, events 4697/7045, Sysmon 12, event 4663, etc. -->

The final task is to ask yourself "is there another way to do any of these operations?" For example, is there another way to open a handle to a remote SCM besides calling OpenSCManager? Can we call an RPC on the target machine directly instead of using CreateService? Could we create a registry key on the remote system without involving SCM at all?

If these questions lead you to other possible paths or operations, add them to your DDM.

## Using a DDM

Now that we've completed the process and have our DDM, it's time to use it. We already accomplished purpose #1: mapping out the operations to ensure we have a detailed and complete understanding of how the technique works. Now we accomplish purposes #2 and #3.

### Distinguish between Unique Procedures

It's time to use our DDM to determine if it includes distinct procedures. I'm a believer in Jared Atkinson's definition of a procedure (see "[What is a Procedure](https://posts.specterops.io/on-detection-tactical-to-function-810c14798f63)" for details): a procedure represents a unique series of operations that accomplish the technique. This is part of why it's important that a DDM only includes **essential** operations! Including optional operations makes it harder to distinguish procedures.

If you have two very different paths through your DDM, you probably have two different procedures. For example, if we determine that an attacker can create a service remotely by connecting directly to the remote registry, our DDM looks like this:

<!-- Image: DDM showing two separate paths - one through SCM and one directly through "Create Remote Registry Key" to "Create Registry Key" -->

It's visually very obvious that the path from "Create Remote Registry Key" to "Create Registry Key" is entirely separate from any of the other operations. That tells us we have two unique procedures: creating a service via SCM, and creating a service via the registry. (Now, if you've been paying attention, you're probably thinking that new "Create Remote Registry Key" operation above is very likely a summary of other operations, and you're correct. We need to do more iterations until we understand what's really happening there, but I'll leave that as an exercise for the reader.)

Generalizing this, any time we have 2 or more distinct paths through a technique, we're probably looking at 2 procedures. The following operation map has two distinct procedures: one via B and one via C.

<!-- Image: Simple diagram showing A branching to B and C, both leading to D - illustrating two distinct procedures -->

At this point, you may want to fork the DDM into two — one for each procedure identified — and then dig deeper into the new procedure until you really understand it. On the other hand, if your telemetry allows you identify both procedures with a single source, you might want to keep them in a single DDM. More on telemetry next….

### Choose the Telemetry Source with the Most Accurate Identification

Decide which data source offers the best bet at accurate identification of the technique. That will often be the source closest to the end of the operation chain. With our example technique, it seems like our best source would be Sysmon 12 or a SACL on the SCM database in the registry. That would allow us to identify new services with near 100% accuracy, even if an attacker created a registry key directly without using RPC. However, if neither of those is an option in your environment, the next best choice would be events 4697 or 7045. At that point, we're best forking our DDM into two different procedures. We would have very good identification for one of procedures (the one using SCM), but we would also know we have an identification gap on the other procedure (using the registry). This is often the case with threat detection, so at this point we'll just document the gap and move on. The goal is to [cover as many dots as possible](https://medium.com/@vanvleet/threat-detection-strategy-a-visual-model-b8f4fa518441), but we know we can't cover **all** of them. At some later point, if we gain the ability to set SACLs or deploy Sysmon, we can circle back to this procedure.

## Wrapping it Up

I have explained why we need DDMs and how to make them. Now I'm going to return back to where I started, with the DDM for CVE-2023–23397. Remember that operation that was simply a question mark? I left that there to make a point. Sometimes, we may find that a DDM has already given us the information we need to identify the procedure with high accuracy. For example, maybe our email security solution allows us to flag every incoming message that contains "*PidLidReminderFileParameter"* and we know from our research that the field is absolutely necessary for the attack technique to work. At that point, you might decide to call the DDM **good enough** for your purposes. Remember this is a tool, not a end to itself.

However, if you haven't already identified an excellent source for accurate identification, that question mark might represent the perfect identification opportunity that you just don't know about yet. Imagine if in our example we stopped at the first layer and our DDM looked like this:

<!-- Image: Simple DDM showing only top-level operations with question marks for unknown details -->

We would be entirely ignorant of the opportunity provided by events 4697 and 7045 and might conclude that without Sysmon or a SACL, we can't identify this technique at all and put it on the shelf. Or, in the case of CVE-2023–23397, perhaps we cobble together a low fidelity detection based on SMB and WebDav traffic because it's the best we have available. It may be, and it may not be… it all depends on what's behind the question mark. **One important benefit of a DDM is to help us realize that there IS a question mark in our understanding of a technique, so we can make an informed decision about what our best option is.**

## Thoughts?

Hopefully this article has provided you with a tool that can help with your next attempt to identify an attack technique in your environment! If you have any questions or thoughts to add, post a comment below.

---

**Tags:** Threat Detection, Detection Engineering, Detection Data Model, Detection Modelling