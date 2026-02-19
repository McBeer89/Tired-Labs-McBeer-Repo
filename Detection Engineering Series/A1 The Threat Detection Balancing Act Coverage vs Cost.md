# The Threat Detection Balancing Act: Coverage vs Cost

**Author:** VanVleet  
**Published:** January 23, 2024  
**Reading Time:** 7 min read  
**Part of:** [Threat Detection Engineering: The Series](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62)

![VanVleet Profile](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

---

<!-- Image: Article header image - not accessible -->

This article is part of a [series on Threat Detection](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62), if you haven't read the earlier articles, you might want to do that first.

As discussed in my [article on strategy](https://medium.com/@vanvleet/threat-detection-strategy-a-visual-model-b8f4fa518441), threat detection is like a game of probability: we try to build preventative mechanisms and detections that cover enough of the attack surface that it's unlikely an attacker will find a path through our network without triggering one of our alarms and alerting us to their presence. In this post, I'm going to explore some of the practical realities and constraints involved in maximizing our attack surface coverage and the implications for threat detection efforts.

At first blush, the best approach seems to be to deploy as many detections as possible, maximizing our coverage through overwhelming numbers. This approach is facilitated by the many available collections of public or commercially-provided detection content. For example, Elastic Security [advertises](https://www.elastic.co/blog/elastic-detection-rules-open-visibility-data-quality) 800 SIEM rules plus 380 endpoint rules in their version 8.8 release. [Anvilogic](https://www.anvilogic.com/) and [SOCPrime](https://socprime.com/) and claim thousands of ready-to-go rules. Sentinel offers [50+ rules](https://github.com/Azure/Azure-Sentinel/tree/master/Detections/AuditLogs) for protecting Azure AD alone. It is relatively easy to deploy detections for many thousands of use cases, especially when you're trying to protect a wide range of enterprise systems: endpoints running any of the top 3 operating systems, network devices, orchestration platforms, cloud platforms, Active Directory, and so on.

## Detections: A Limited Resource

While an automation platform might support a huge number of detections, **in practice there are constraints on the number of detections that a given organization can maintain.** Every deployed detection is going to generate a certain number of false positive (FP) alerts. Some detections might identify rare or easily distinguished malicious activity and almost never generate FPs, while others may be trying to spot malicious use of common resources and generate frequent FPs. But EVERY deployed detection will generate a least a few.

For the sake of discussion, let's assume that on average a given body of detections will generate only one FP per month per alert. At that rate, a body of 500 alerts will generate 500 FP's each month. (For this calculation, we won't count true positive alerts: if you have more true positive alerts than resources to handle them, your problems aren't with Threat Detection!) Now, let's assume that our incident responders can investigate those false positives at a rate of 1 every 30 minutes, all day every day without burning out and quitting. That means one responder can handle 16 alerts per day, and 320 alerts per month. So, our body of 500 alerts will require a team of 2 responders just to manage the false positives (to say nothing of handling true positives!). This simplistic example scales linearly: 1000 deployed detections will need a team of 4 responders, 1500 will need 6, etc.

In addition to the cost in incident response time, each detection also requires care and feeding from the Detection Engineering team. For every alert deployed, there is some amount of time that must be spent on maintenance: creating filters for recurring false positives, updating and fixing queries that break due to things like log source changes. There should also be a validation process to ensure that all of those hundreds or thousands of detections are still working as designed, otherwise your real detection capability will atrophy over time.

Each detection also carries costs in automation platform resources: the processing and memory required to run a detection query every X minutes, 365 days a year, in order to alert as quickly as possible when the malicious activity it's looking for actually happens. We're not going to explore those costs here, since they vary drastically from configuration to configuration.

**All of this means that for any given organization, there is an upper ceiling on the number of detections that can be deployed and maintained.** They are a limited resource. While our example is simplistic, [industry surveys](https://swimlane.com/blog/top-soc-analyst-challenges/) suggest the assumptions we used to inform it probably aren't too far off. I'd guess from my own experience that for most organizations, the limit is likely between 1500–4000 deployed detections.

## Incremental Coverage vs. Incremental Cost

The cost of one new detection, in terms of response and investigation time, care and feeding, and query platform resources, can be considered the detection's **incremental cost**.

In the [strategy article](https://medium.com/@vanvleet/threat-detection-strategy-a-visual-model-b8f4fa518441), I explored various detection patterns and offered a model to think through how much total attack surface a given detection covers. I'm going to use the term **incremental coverage** to describe how much additional attack surface coverage one detection provides. Here are a few details from that previous post that you'll need to know now: we're going to suppose that there are only 500 procedures in our total attack surface. (Mitre's ATT&CK matrix v13 defines 196 attack techniques and 411 sub-techniques, so our theoretical is definitely simpler than real life, but it makes the math easier without compromising the argument. I'd guess there are closer to 1000 distinct procedures in the real world.) Using this estimate, we can do some rough incremental coverage calculations:

* A detection that comprehensively covers one procedure would provide incremental coverage of about 1/500th.
* A 'tuple' detection (one that looks for a combination of two or more procedures) yields incremental coverage of 1/124,750th (there are 124,750 possible 2-tuples of 500 procedures).
* A 'tangential' detection (one that looks for an attacker-controlled element, like a command line) adds 1/500,000th of incremental coverage at best (an attacker can modify the attack to evade the detection endlessly, but we're going to cap the possible modifications at 1000 per procedure so we can assign it an incremental coverage value).

When we compare incremental cost to incremental coverage, it becomes evident that some detections probably aren't worth it. For example, let's imagine our organization's maximum detection limit is 6000 (I'm high-balling the estimate to emphasize the point) and we onboard 3000 off-the-shelf detections from our favorite public or commercial repository. If those 3000 are all entirely 'tangential' detections, then we have improved our attack surface coverage by about 3000/500000ths, or 3/500ths. But those detections have consumed 1/2 of our total available detection capacity! That leaves only 1/2 our capacity to cover the other 497/500ths of the attack surface! Clearly, this is a losing strategy. Under this scenario, there's a high probability that an attacker can find a path through our network that we don't have covered.

## From Theoretical to Reality

We've used a lot of estimates to create our model and simplify the math. The real numbers are going to vary per organization. Your actual false positive rate, and therefore the incremental cost per detection, will depend on your environmental noise, quality of your telemetry, and the skill of your detection engineering team. The number of alerts that your incident response team can handle depends on their tooling, automation, skill, and experience. But the real-world attack surface is also much larger than our theoretical case, so the constraints and trade-offs highlighted here are definitely still in force in real life, if not more so. **The attack surface is large enough (especially considering all the different platforms a typical organization has to defend!) and the real-world limit on detections low enough that it is important to maximize the incremental coverage and minimize the incremental cost of each detection we deploy.** A big body of detections with low incremental coverage won't help us win the game of probability. We're much better off with a smaller body of detections with high incremental coverage. **From a theoretical standpoint, 3 detections that each comprehensively cover 1 procedure provide the same attack surface coverage (3/500ths) as those 3000 tangential detections, and at significantly lower incremental cost.**

But reality is more nuanced than our theoretical model, naturally. Those 3000 'tangential' off-the-shelf detections, assuming they are well distributed amongst the various techniques, might actually provide very good detection coverage against low-skilled attackers like 'script kiddies' or threat groups who mostly pursue low-hanging fruit. If the attackers targeting your organization are all likely to use off-the-shelf attack tools and techniques without obfuscation or modification, then those 3000 off-the-shelf detections could be exactly the right strategy. On the other hand, they'll be next to worthless against an attacker who is careful NOT to use known command line parameters and obfuscates their tooling. State-sponsored attackers and skilled criminal actors will have no difficulty evading those 3000 'tangential' detections, **leaving your organization *feeling* protected but effectively defenseless.** In that case, you're much better off with those 3 comprehensive detections.

## Summary

While it might appear that detection capacity is infinite and therefore any additional detection is worth deploying, in reality detections are a limited resource. Detection Engineers should maximize the incremental coverage and minimize the increment cost of each detection they deploy to ensure that they cover as much of the total attack surface as comprehensively as possible. Large collections of detections that offer little incremental coverage may give an organization the illusion of protection, but leave them effectively defenseless.

## One Final Thought: An Ounce of Prevention….

While not the main topic of this article, this discussion highlights the value of policies and mechanisms that prevent attack techniques outright. For example, if you're working to defend a Kubernetes cluster and you can put a policy in place to completely prevent the creation privileged containers, then you have reduced the total attack surface with very little incremental cost. Same for features like Windows Credential Guard to prevent credential-theft techniques targeting LSASS. Those are big wins! Preventative measures are the only thing that can improve the fundamentally disproportionate relationship between attack surface (huge) and detection capacity (too small). **While we don't often think of prevention as part of Threat Detection, it ought to be the first thing a Detection Engineer considers when evaluating how to deal with an attack technique.** (Note, you shouldn't disable a detection because you are preventing the attack! There is value in knowing something was attempted, even if it was prevented. But by preventing something outright, you significantly reduce the incremental cost of that detection: it shouldn't fire unless something goes REALLY wrong.)

## Thoughts?

I'd love to hear if your experience is consistent with or different from my own. If you have any thoughts to add, post a comment or let me know on [Twitter](https://twitter.com/_vanvleet)!

*Originally published at [https://www.linkedin.com](https://www.linkedin.com/pulse/threat-detection-balancing-act-coverage-vs-cost-andrew-vanvleet).*

---

**Tags:** Threat Detection, Detection Engineering, Information Security