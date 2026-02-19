# Mistaken Identification: When an Attack Technique isn't a Technique

**Author:** VanVleet  
**Published:** July 1, 2024  
**Reading Time:** 6 min read  
**Part of:** [Threat Detection Engineering: The Series](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62)

![VanVleet Profile](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

---

This article is part of a [series on Threat Detection](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62). In this post, I'm going to talk about one of the challenges Detection Engineers face: sometimes a Mitre ATT&CK technique isn't really a technique at all, which really complicates trying to detect it! I'm going to use T1059.001 PowerShell as my example in this article, but the concept applies to a lot of other techniques (too many!). Ultimately, we'll demonstrate why T1059.001 (and many others) shouldn't even exist.

If you haven't already read my articles on [Identifying and Classifying](https://medium.com/@vanvleet/identifying-and-classifying-attack-techniques-002c0c4cd595) and [Detection Data Models](https://medium.com/@vanvleet/improving-threat-identification-with-detection-data-models-1cad2f8ce051), you might want to start there so it's easier to follow along.

## Let's Get Started

Let's imagine that you were looking over the top attack techniques used in 2023. Red Canary has an excellent site called ["Threat Detection Report"](https://redcanary.com/threat-detection-report/) that gives lots of great insights into the top attack techniques they're seeing. Directly from their site, "The following chart represents the most prevalent MITRE ATT&CK® techniques observed in confirmed threats across the Red Canary customer base in 2022."

<!-- Image: Red Canary Threat Detection Report chart showing top MITRE ATT&CK techniques, with Windows Command Interpreter and PowerShell at the top positions -->

The top two techniques they saw in 2022 were Windows Command Interpreter and PowerShell. If your leadership team saw this page, there's a fair chance you're going to get a question on what your company's detection posture is for these techniques! So, being proactive, you jump into the task of figuring out how to defend against it. You decide to start with T1059.001 PowerShell, and having recently read my article on DDMs, you're a devoted convert to using them to understand and identify a technique. :) So, you get started building your DDM.

## Building a DDM for T1059.001 PowerShell

You pull up your drawing app and start to plot out the operations for T1059.001 PowerShell. The first operation is…. Um….

<!-- Image: Empty DDM diagram showing confusion - no clear starting operation for "PowerShell" as a technique -->

You have no idea what to put down here, because "PowerShell" tells you absolutely nothing. It's like if someone said "The bad guys are going to use a computer to rob the bank, now go stop them!" There are any number of ways they could be using the computer, from throwing it through a window to an *Oceans 11-*style takeover of the entire system.

## Tools, not Techniques

The problem with an attack technique of "PowerShell" (or Windows Command Interpreter or WMI) is that we haven't actually defined an **attack**. We've only defined a tool, one used by attackers and admins alike. An attacker uses PowerShell to **do** something, like establish command and control, exfiltrate your data, move laterally, or elevate privileges. The sentence "the attackers used PowerShell" is worthless unless it's followed by "to accomplish X." What's really happening here is that PowerShell is the tool and X is the actual attack technique they used it for.

The InfoSec industry doesn't have any difficulty identifying something like MimiKatz or CobaltStrike as a tool, but for some reason ATT&CK really struggles with general-purpose tools like PowerShell, Python, WMI, DLLs and Shared Modules, operating system APIs, cloud APIs, etc.

***A Side Note:*** *I think the case could be made that the entire Execution Tactic shouldn't exist. The problem is similar: execution isn't an attacker objective, it's the way an attacker achieves the other objectives. "Execution" doesn't stand alone. You execute code to do something, and the something is the objective. By gaining initial access, it is implied that you have gained execution somewhere in the network. Additional executions all have additional objectives: move laterally, elevate privileges, exfiltrate data. Most, if not all, of the techniques listed under the Execution tactic are actually tools. The problem of defining tools as techniques probably has its origin in the mistake of defining "Execution" as an objective.*

## Trying to Detect Tools

We confuse ourselves when we define tools as techniques. It makes the ATT&CK framework a bit difficult to work with for detection engineers. When we try to take on the job of detecting a tool instead of a technique, we have one of two problems:

1. If the tool is narrowly focused, like Mimikatz, then we're detecting something tangential and attacker-controlled. As discussed in previous articles, our detection provides little incremental coverage because an attacker can use any tool they want, with an infinite list of options.
2. If the tool is broadly capable, like PowerShell, then we're trying to detect EVERYTHING, as implemented in one specific tool. That is not only a daunting task, it's also very inefficient. If we're going to try and detect every technique, we're better off focusing on detecting the technique itself, including but not limited to implementations that use one specific tool.

**Either way, a focus on the tool over the technique leads to bad detection engineering.** It has a strong likelihood of pushing us towards tangential detections with poor incremental coverage. Focusing on detecting tools, even very capable and frequently-used tools like PowerShell, shifts the game of probability to the attacker's favor. They can, after all, always use a new tool, rendering all our tool-focused detections worthless.

## How to Distinguish Tools from Techniques

For detection engineers, we need to be able to determine when a technique is really a tool so we don't expend valuable time and effort trying to detect it. I would offer this as my litmus test: **an attack technique must be focused on an actual attack (something that achieves a specific attacker objective) and can be defined as an operation chain (even if it's a chain of one!).** Think about it: if it can't be mapped, it can't be identified. And if it can't be identified, it can't be detected!

I think a good example of this distinction can be seen with T1546.003 WMI Event Subscription (for Persistence or Priv Esc) compared with T1047 WMI. The first is a specific action that accomplishes a specific attacker objective: to gain persistence or to elevate their privileges. We can map out the operation chain:

<!-- Image: DDM for T1546.003 WMI Event Subscription showing clear operation chain: Create Event Filter → Create Event Consumer → Create Binding -->

The second is as exactly the same as PowerShell: we don't have any idea what an attacker actually did when we say "they used WMI." It could be anything, it could be nothing. It could be malicious or benign. It's not focused on an actual attack and it cannot be defined as an operation chain. It's a tool, not a technique.

## The Case for Detecting SOME Tools

While I've argued against spending time on tool-based detections, there are some tool-based detections that might be worth the cost of developing and maintaining. Some tools are very frequently abused by real-world attackers (CobaltStrike, for example) and sometimes attackers use them in ways that are really suspicious in your particular environment (most LOLBins and maybe highly obfuscated or frequently abused PowerShell commands, for example). In those cases, even though an attacker can theoretically use any tool and render your detections worthless, the frequency with which those are actually being abused makes them a fair candidate for a tool-specific detection, so long as their incremental cost isn't too high.

## Summary

The ATT&CK framework is useful to detection engineers because it helps us catalog known attack techniques and then methodically research and detect them. However, ATT&CK mistakenly identifies numerous tools as techniques, making a detection engineer's life harder. Focusing on tools instead of techniques makes defending more difficult, because ultimately the attacker gets to choose the tool. You can distinguish techniques that are really tools by determining if they are focused on achieving a specific attacker objective and can be defined in an operational chain. Techniques that are really tools are best left alone, focusing instead on comprehensively detecting the real techniques, regardless of the tool used to implement it.

Hope this was useful to you! If you have any questions or thoughts to add, post a comment below.

---

**Tags:** Threat Detection, Mitre Attck, Powershell, Cybersecurity, Detection Engineering