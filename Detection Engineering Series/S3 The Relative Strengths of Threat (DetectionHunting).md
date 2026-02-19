# The Relative Strengths of Threat (Detection|Hunting)

**Author:** VanVleet  
**Published:** January 23, 2024  
**Reading Time:** 8 min read  
**Part of:** [Threat Detection Engineering: The Series](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62)

![VanVleet Profile](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

---

This article is one in a [series on Threat Detection](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62). Here, I'll attempt to disambiguate the terms "threat hunting" and "threat detection" and explore the areas where each practice has relative strengths.

## **Threat Hunting, Threat Detection, Detection Engineering?!?**

There are a lot of terms in the industry for the processes we use to prevent threats from impacting our networks. For me personally, there are 3 that seem to involve a lot of confusion about where one ends and the next begins: threat hunting, threat detection, and detection engineering.

A few definitions from well-respected industry sources (added emphasis is mine):

* "Cyber threat hunting involves **proactively searching** organizational systems, networks, and infrastructure for advanced threats. **The objective is to track and disrupt cyber adversaries as early as possible** in the attack sequence and to measurably improve the speed and accuracy of organizational responses." — NIST SP 800–172
* "Detection engineering is the **process of identifying threats before they can do significant damage.**" -Crowdstrike
* "Threat detection is the practice of **analyzing the entirety of a security ecosystem to identify any malicious activity** that could compromise the network." -Rapid7
* "Threat hunting is an **active** IT security exercise with the intent of **finding and rooting out cyber attacks that have penetrated your environment without raising any alarms.**" -Cisco
* "Threat detection is the process of **identifying threats in an organization** that are actively trying to attack the endpoints, networks, devices and systems." -Splunk

See any similarities there? No wonder we can't figure out which one is which! All three terms essentially mean "an effort to find undetected threats in a network as soon as possible." One could argue that the terms are practically synonymous.

There IS a distinction between Threat Hunting and Threat Detection, but the massive overlap between them stymies efforts to define them in a way that clearly differentiates. There are a huge range of activities and approaches that fall under both domains. If you like Venn diagrams (and I do!), here's what this one might look like:

<!-- Image: Venn diagram showing overlap between Threat Hunting and Threat Detection -->

I think it would take an immense effort to get the entire InfoSec industry to agree on a single definition for each, so I'm not going to attempt to draw a defining boundary today. My goal is to suggest an approach that leverages their relative strengths. But, because some kind of distinction is needed to compare and contrast them, I'm going to loosely define Threat Detection as the process of **building** **automated** **alerting** for threats, and Threat Hunting simply as **actively searching** for threats.

It is import to note that while threat hunting and threat detection are both capable of covering a lot of the same space, **they are two different approaches with different constraints, relative advantages, and outcomes.** When you are intending to create a detection, you need to be confined to data that you can collect, parse, enrich, and search in an **automated** fashion. **But threat hunting should not be constrained by the bounds of automation.** You can do things that can't be automated, like pulling data you don't normally collect, enriching it in ways you can't do at SIEM ingest, and analyzing it with a script that runs for a full week, then manually reviewing to see if anything just doesn't feel right. Threat hunting can go anywhere it needs to and take as long as necessary, that's what makes it powerful. To bind threat hunting with the same constraints as threat detection ties its hands and makes it less capable of accomplishing the very thing it excels at: sorting through anomalous activity to find the things that might've slipped through.

AND, if you ARE bounding yourself to the constraints of threat detection in the hopes that your hunt might lead to an automated detection, what you are doing is probably more closely aligned with threat detection. To mangle Shakespeare, "Threat detection by any other name will still ideally produce an automated detection." You would likely get better value from your efforts by following an intentional threat detection methodology, then revisiting your threat hunting efforts to release them from the automation constraints.

As for how Detection Engineering fits into the picture, I think it's the process by which Threat Detection is accomplished. I like [Florian Roth's definition](https://cyb3rops.medium.com/about-detection-engineering-44d39e0755f0) of it:

*"Detection engineering transforms an idea of how to detect a specific condition or activity into a concrete description of how to detect it."*

Detection Engineering is concerned with the best practices of Threat Detection: how to do it and how to do it well. I will therefore use the term "Threat Detection" to encompass both.

## What Threat Hunting|Detection Are NOT

I know it's bold to declare something the "wrong way," but I'm going to go out on a limb and argue that there are a few things commonly referred to as threat hunting or threat detection that really are wrong applications of the terms.

* **IOC "Hunting" —** Many public articles on Threat Hunting describe the IOA/IOC/TTP approach: you take a known indicator (be that a hash, URL, or ATT&CK technique) and you hunt in your network to see if it's present. This is a valid way to "actively search for threats" and would thus qualify as Threat Hunting. However, while valid under the loose definition, this kind of hunting is **inefficient.** If you can define what you're looking for as concretely as a hash, URL, or technique, and you can find a way to confidently determine if it's present in your network, you really should be creating an automated detection to alert you whenever it turns up. But if you build an automated detection for it, at that point it's most accurate to describe the process as Threat Detection. And if you put in all the effort to determine if a given IOC/IOA/TTP is present or not at a given time without then creating an automated detection, that's best described as ineffective Threat Detection rather than Threat Hunting.
* **"Pulling the Thread" —** I cannot count the number of "Threat Hunting" vendor webinars and presentations I've attend that ended up being about responding to a suspicious event in your environment. I would argue that if you're starting with a known, suspicious event that ALREADY HAPPENED, you're not doing threat detection or threat hunting. You're doing incident response. Threat Hunting and Detection are about finding the things you DON'T already know about. Incident Response is the practice of dealing with those you DO.

## **Relative Advantage: Malicious vs. Anomalous**

Now let's focus in on Threat Detection and Hunting specifically. Given the overlap between the practices of Threat (Detection|Hunt), perhaps the best question is then "where are their relative advantages?"

* Threat Detection's relative advantage is for dealing with things (sub-techniques!) that we can define as likely **malicious** and build high-fidelity automated detections to alert us any time they happen. If we can't make a high-fidelity determination, we end up with many false positives threatening alert fatigue.
* Threat Hunting, on the other hand, doesn't require as much fidelity. It is perfectly comfortable with identifying **anomalous** activity, and then determining if that activity is malicious in nature. The process of investigating hunting leads doesn't have to be automatable, nor does it need to be high-fidelity. Threat Hunters, who should be experts in their own terrain, can explore anomalous findings and determine if they are caused by a network quirk, a misconfiguration or an attacker trying to stay out of sight. It is possible, for example, to hunt based on a hypothesis like "someone in our network is sending data to somewhere it doesn't belong." The hunter could pull network logs and begin to crunch data and figure out what is flowing where, and whether or not it belongs there. However, it would be VERY difficult to build an automated detection for that, because "where it doesn't belong" is subjective and requires a lot of home-turf expertise.

To put it another way, anything that can be determined with adequate confidence to be **malicious** in an automated way is most effectively dealt with through Threat Detection. Anything that can only be determined to be **anomalous** is best handled through Threat Hunting.

Another relative advantage is that Threat Detection provides continuous threat monitoring whereas Threat Hunting provides only a point-in-time check. Hunting might identify intruders or gaps that need to be fortified, but it might yield nothing. Either way, it is necessary to keep sending those scouting parties out, even to the same regions they previously scouted, to ensure nothing has changed since the last check.

Finally, Threat Detection lends itself to metrics and measurement better than Threat Hunting. It's much easier to demonstrate the value of increased coverage against known techniques than it is to demonstrate the value of a hunting foray that turns up nothing.

## **The Best of Both Worlds: The Relative Advantages Strategy**

We can get the best of both worlds by using each process where it has a relative advantage. Because of its strengths in continuous monitoring and easier metrics, the most effective approach is to handle everything we CAN through Threat Detection, and Threat Hunt the things that Detection isn't well suited to handle. Trying to represent this "relative advantages" strategy in our original Venn diagram would look something like this:

<!-- Image: Modified Venn diagram showing the relative advantages strategy - Threat Detection handling malicious activities, Threat Hunting handling anomalous activities -->

This strategy dictates a robust Threat Detection program working to identify and fill gaps for all known, definable **malicious** activities and providing continuous monitoring for them through automated detections. Alongside this Threat Detection program is a Threat Hunting program that actively searches for **anomalous** activities and determines whether the source is malicious in nature to make sure no one has managed to sneak through undetected.

## Summary

While both practices could be reasonably applied to a wide range of activities, Threat Detection holds a lot of advantages when a threat can be defined, declared malicious with reasonable confidence, and detected in an automated fashion. Threat Hunting excels in identifying anomalous activity that requires further investigation to classify as malicious or benign, and it is most powerful when freed from the constraints of automation. A Blue Team should apply both of them to the problems where they are most effective.

## Thoughts?

The world of Threat Hunting/Detection is pretty big! I'd love to hear thoughts or other ways of structuring things that you've found effective. If you have any thoughts to add, post a comment or let me know on [Twitter](https://twitter.com/_vanvleet)!

## **Credit Where It's Due**

Many of these ideas were clarified in my mind through numerous conversations with my exceptional colleagues Stephanie Copley, Steve Brawn, and Christopher Simpson.

## **Sources**

* https://www.crowdstrike.com/cybersecurity-101/threat-hunting/
* https://www.splunk.com/en_us/blog/learn/threat-hunting-vs-threat-detecting.html
* https://www.crowdstrike.com/cybersecurity-101/observability/detection-engineering/
* https://en.wikipedia.org/wiki/Cyber_threat_hunting
* https://cyb3rops.medium.com/about-detection-engineering-44d39e0755f0
* https://csrc.nist.gov/csrc/media/Publications/sp/800-172/final/documents/sp800-172-enhanced-security-reqs.xlsx
* https://sysdig.com/learn-cloud-native/detection-and-response/what-is-threat-detection-and-response-tdr/
* https://www.rapid7.com/fundamentals/threat-detection/
* https://www.cisco.com/c/en/us/products/security/endpoint-security/what-is-threat-hunting.html

*Originally published at [https://www.linkedin.com](https://www.linkedin.com/pulse/relative-strengths-threat-detectionhunting-andrew-vanvleet).*

---

**Tags:** Threat Hunting, Threat Detection, Information Security, Detection Engineering