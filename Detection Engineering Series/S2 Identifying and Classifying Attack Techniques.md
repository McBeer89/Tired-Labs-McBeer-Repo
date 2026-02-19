# Identifying and Classifying Attack Techniques

**Author:** VanVleet  
**Published:** February 14, 2024  
**Reading Time:** 7 min read  
**Part of:** [Threat Detection Engineering: The Series](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62)

![VanVleet Profile](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

---

<!-- Image: Article header image - not accessible -->

This article is part of a [series on Threat Detection](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62). In this post, we'll focus on the challenge of identifying and classifying events in order to detect a given attack technique.

*Update 8/29/2024: I know we're all standing on the shoulders of giants as we improve our understanding of and skills in detection engineering, but in the case of this article I've discovered that Jared Atkinson wrote about the idea of the two primary tasks of identification and classification a few* ***years*** *before me. Definitely recommend giving* [*his article*](https://posts.specterops.io/thoughts-on-detection-3c5cab66f511) *a read! Thanks, Jared, for letting me stand on your shoulders so often!*

## The Two Primary Tasks

When trying to detect an attack technique, there are two primary tasks that a Detection Engineer has to accomplish:

1. Identify when an event that is integral to an attack technique occurs in their environment.
2. Classify each identified event as malicious or benign.

Both tasks must be done successfully in order to detect the attack. For example, if we can identify with 100% accuracy that a scheduled task ([T1053.005](https://attack.mitre.org/techniques/T1053/005/)) is created, but we can't classify each new task as malicious or benign, we can't detect this technique. Alternately, perhaps we can classify a Golden Ticket ([T1558.001](https://attack.mitre.org/techniques/T1558/001/)) with 100% accuracy, but we have no telemetry to identify it. In either case, we cannot successfully detect attacks using that technique. In real life detection scenarios, we often end up with mixed results: perhaps we can identify 80% of the events, and of those we can classify 80%, giving us a 64% probability of detecting a specific malicious instance. **The more accurate we can get in either category, the better our probability of detecting a malicious instance of the target attack technique.**

## An Environment Specific Job

If you ever wondered why every company has to hire their own detection engineers, or why there isn't some universal solution to detecting known attack techniques, the reason is that identification and classification are both *very* environment specific. **Identification depends heavily on what sources of telemetry a given company has available. Classification requires filtering the malicious signal from the noise in a given environment.**

The Mitre ATT&CK matrix does a fair job of cataloging attack techniques, but it's up to detection engineers to figure out how to detect those techniques given the set of telemetry and noise in their enterprise. A detection that is highly effective for one enterprise might be unworkable for another because they don't have the same telemetry or they have completely different environmental noise.

## Identifying

When identifying techniques it is critical to focus our identification on essential and immutable elements. If we use tangential elements or those an attacker controls, then our identification accuracy plummets and the probability of detecting a given malicious instance drops with it. Elements that an attacker controls are likely to be changed precisely in the instances that we are most likely to be interested in.

By way of example, let's look at using a WMI Event Subscription (T1546.003) for persistence. Here's a model of how that technique works and some available telemetry (Sysmon). It's a simple technique: you create an event consumer and filter, and a binding to connect them together. The binding has to come last (you can't bind something that doesn't exist).

<!-- Image: Diagram showing WMI Event Subscription process flow with Event Consumer, Filter, and Binding components -->

Our goal is to identify 100% of the times that an Event Subscription is created. If we focus on the command line parameters an attacker might use (which are both tangential and attacker-controlled, so your Spidey-sense ought to be tingling already), it's going to be impossible get to 100% accuracy.

<!-- Image: Diagram comparing identification methods - command line parameters vs Sysmon Event 21, showing infinite command line variations vs single essential telemetry point -->

In fact, it would take an immense effort to approach even 1% identification accuracy. This is due to the fact that there are literally infinite command lines an attacker can use to create a WMI Event Subscription. They could use existing scripts or tools, write their own script or binary, obfuscate the command line parameters, etc.

On the other hand, we could get almost 100% accuracy if we use Sysmon event 21. It is an essential and immutable step in the technique.

This example is a detailed illustration of what hopefully was already obvious: it's really important that we choose the right telemetry to identify events for a detection. Even if we can classify with 100% accuracy, we'll end up with a 1% chance of identifying a given attack technique if we take the wrong approach to identifying. **Accurate identification is absolutely critical to good detection engineering.** It is also difficult, and one of the areas where I see the most mistakes in public or commercial detection repositories. In another article, I'm going offer an analytic tool that helps to do it well: [detection data models](https://medium.com/@vanvleet/improving-threat-identification-with-detection-data-models-1cad2f8ce051).

## Classifying

Once we've identified instances of the technique it is time to classify them. Techniques will fall into one of 3 classification categories: **Inherently Suspicious**, **Suspicious Here**, or **Suspicious in Context**

**Inherently Suspicious** is easy to classify. The vast majority of instances will be malicious, so we can simply assume that any given instance is malicious. These lend themselves well to detections. Things like dumping LSASS, accessing the ntds.dit, and encrypting and replacing shared files are **inherently suspicious**. No legit user should be doing them.

**Suspicious Here** events are also easy to classify. Without legitimate use cases in your given environment, you can also assume that any given instance is malicious. You should note, however, that it's possible a future legit use case might be introduced, moving the technique into the *Suspicious in Context* category. Things like an ActiveScript WMI event consumer or a particular [LOLBin](https://github.com/LOLBAS-Project/LOLBAS) might be **suspicious here**, meaning that in *this* environment, they are highly likely to be malicious because we don't employ them in any legit use case.

**Suspicious in Context** is much harder to classify. Because there are legitimate instances of the technique in the environment, classification requires distinguishing between a malicious and benign instance. For some techniques, this may be impossible to do with adequate accuracy, and the technique is better handled as a warning signal (to be coupled with other signals), rather than as a detection. Things like creating a new service or startup key, running a file remotely, or scanning the network are **suspicious in context**: they might be suspicious, depending on the context in which they take place, but there are also regular benign instances of them here.

## Don't Compete with Your EDR

In my experience, *inherently suspicious* techniques are the bread and butter of EDR companies. Because they are almost always malicious, the identify/classify problem collapses down to mostly an identify problem. EDRs have a definite advantage in collecting telemetry, since they (hopefully!) already have an agent on every one of your enterprise's endpoints. If the EDR's engineers can find a way to collect the right telemetry, they can detect these kinds of techniques with high confidence.

On the other hand, *suspicious here* techniques get harder for them, because they will likely have a large, diverse customer set. What is suspicious in one customer's environment might be business critical in another's, so they can't detect these techniques without potentially creating a lot of noise for some customers. *Suspicious in context* techniques become almost impossible for an EDR provider to detect. They might be able to provide useful telemetry, but there's no way they can raise an alert on these techniques.

There is no point in competing with your EDR. Remember, the [winning strategy is to cover as many techniques as possible!](https://medium.com/@vanvleet/threat-detection-strategy-a-visual-model-b8f4fa518441) As a result, **detection engineers will likely get the most impact by focusing on techniques that are *suspicious here* or *suspicious in context.*** A detection engineer knows their environment best and is in a great position to be able to classify these kinds of events and create coverage where an EDR cannot. (That said, don't assume your EDR has coverage for an *inherently suspicious* technique! Run some tests to verify their coverage, and build a detection to fill any gaps you find.)

## Summary

In order to detect an attack technique, you have to first identify that an event of interest happened, then classify that event as malicious or benign. Both tasks are critical to effective detection; poor outcomes in one can't be balanced by the other. These tasks depend on the available telemetry and noise in a given environment, so they have to be custom tailored to each environment. Detection Engineers shouldn't compete with their EDR solution: they should determine what existing protections they have and fill in gaps. Gaps are most likely to exist with techniques that are suspicious in the context of their own environment, rather than those that are inherently suspicious (which your EDR vendor should be good at detecting, if they're worth what you're paying for them).

## Thoughts?

If you have any questions or thoughts to add, post a comment or let me know on [Twitter](https://twitter.com/_vanvleet)!

---

**Tags:** Threat Detection, Detection Engineering, Information Security