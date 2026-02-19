# Technique Analysis and Modeling

**Author:** VanVleet  
**Published:** March 11, 2025  
**Reading Time:** 6 min read  
**Part of:** [Threat Detection Engineering: The Series](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62)

![VanVleet Profile](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

---

<!-- Image: Article header image - not accessible -->

As I've built a framework for how to keep our networks safe through threat detection, I've established the overall [strategy](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62) and explained how we can shift the odds [strongly in our favor](https://medium.com/@vanvleet/compound-probability-you-dont-need-100-coverage-to-win-a2e650da21a4) using thorough (sub)technique-focused detections.

My goal with this article is to pull all of this strategy together and demonstrate a practical analytical process to apply it to real world attack techniques. In this article, I'll walk through how to analyze a technique to identify distinct procedures and create a strategy for building a thorough detection. I recently did a [podcast](https://youtu.be/5DAQkvOyqME?si=vutHl_lQKcGq_95g) where I go through this same analysis process using the Kerberoasting (T1558.003) technique, so there are multiple examples for all learning styles! :)

This analytic process is most effective when it's facilitated by a model. If this is the first time you've heard of technique modeling (also called detection modeling), pause and go read my article on [detection data models](https://medium.com/@vanvleet/improving-threat-identification-with-detection-data-models-1cad2f8ce051) (DDMs). If you just need a refresher, modeling is a tool that helps to avoid the thinking errors that are common when dealing with complex concepts like attack techniques. When you have to map out your knowledge in a model, you quickly discover the areas where your understanding is lacking and assumptions are filling in the gaps (or you're just missing things!). You can also explore the technique visually, helping you see things you might not think of otherwise.

The steps that we'll follow when analyzing a technique are:

1. Start your model by adding in the things you already know.
2. Choose an operation and go deeper. Expand your knowledge.
3. Add what you've learned to your model, adjusting it as needed.
4. Repeats steps 2 and 3 until you're reasonably confident you've gotten it all.
5. Add in available telemetry.
6. Identify any other possible paths through the model.
7. List the distinct procedures.
8. Document your results.
9. Use the model to create a detection strategy.
10. Implement the detection(s).

I covered steps 1 through 6 for the technique *Create or Modify System Process: Windows Service* (T1543.003) in my [article on DDMs](https://medium.com/@vanvleet/improving-threat-identification-with-detection-data-models-1cad2f8ce051) (and in the podcast I go through steps 1–9). So, in order to keep this article short, we're going to pick up where we previously left off with T1543.003. Here was our completed DDM (with some additional detail, since we're taking it all the way through this time):

<!-- Image: Complete DDM for T1543.003 showing all operations, telemetry sources, and multiple procedure paths including Create Remote Registry Key, RPC via TCP, and RPC via Named Pipe -->

*A quick note: To save time in the last article, we did not expand on the "Create Remote Registry Key" operation. In real life, we should. That operation uses the* [*Windows Remote Registry Protocol*](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rrp/0fa3191d-bb79-490a-81bd-54c2601b7a78) *[MS-RRP], another RPC interface. Because that procedure is so different form the rest, we're best covering it in proper detail in its own model (who knows, there may be a more paths to do it than RPC!). But, to save time in this article, we're going to skip analyzing that procedure. That does mean that our detection strategy could be missing opportunities: a good case study in the costs of not analyzing and modeling a procedure.*

## Step 7 — List the Distinct Procedures

We have identified 3 distinct paths through the model, so that's 3 procedures:

1. Create a registry key remotely.
2. Call the RCreateServiceW RPC call using a TCP connection.
3. Call the RCreateServiceW RPC call using a named pipe.

## Step 8 — Document your results.

The next step is to capture the results of your analysis, including your model, for your whole team and for future detection engineers. The goal is to document the distinct procedures along with all the background and technical information necessary to understand how and why those procedures work. This provides the context, information, and telemetry necessary to build a detection strategy to detect the technique as comprehensively as possible. This report can enable any detection engineer to quickly create a thorough detection for the technique in their own environment.

In a future post, I'll share the template that I use for documenting technique analysis, along with some examples. I call them Technique Research Reports (TRRs). But more on that later….

## Step 9 — Use the model to create a detection strategy.

The next step is to employ our model to create a detection strategy. Recall that detecting a technique has two tasks: [identifying and classifying.](https://medium.com/@vanvleet/identifying-and-classifying-attack-techniques-002c0c4cd595) We can only classify events that we have identified, so if we base a detection on a log source that identifies only 50% of the procedures, the very best we can hope for is to cover 50% of the technique's attack surface. We need to detect as many of the procedures as possible, so we're ideally looking for a point in the model that has telemetry and is shared by many or all procedures. Otherwise, we'll need a group of detections that collectively cover all procedures.

On this model, there is one spot that definitely offers better identification than the rest:

<!-- Image: DDM highlighting the "Create Registry Key" operation as the ideal detection point covering 100% of procedures -->

If we can create a detection at the "Create Registry Key" operation, we can identify 100% of the events. Hopefully, we can also find a way to classify those events as malicious with high fidelity, too! (But remember, classification is an environment-specific task: some environments might have so little noise that any new services are suspicious, while others might see new services all the time.) If you can set a SACL or have Sysmon in your environment (or an EDR that provides an equivalent log), you're set!

However, if you don't have any of those then we need to keep looking. The next best option is at the "Receive RPC" operation.

<!-- Image: DDM highlighting the "Receive RPC" operation as the second-best detection point covering 2 of 3 procedures -->

At this point, we can identify 2 of the 3 procedures. The 3rd procedure is going to end up a known blind spot (but that's ok, remember [we don't have to get 100% to win!](https://medium.com/@vanvleet/compound-probability-you-dont-need-100-coverage-to-win-a2e650da21a4)). You have two possible logs to choose from at this operation, so hopefully you find one that works. *(Again, if we delve into that 3rd procedure — creating the remote registry key — we may find some detection opportunities and it wouldn't have to be a known blind spot.)*

But let's keep going a bit further. Imagine that for some reason, you can't get the RPC event logs. At that point, your best strategy is going to be to try and catch the network communications (it's the only option left!). At this spot in our model, there are two paths that we'll have to address separately, so our detection strategy will be pair of complementary detections.

<!-- Image: DDM highlighting network communication operations (SMB Named Pipe and TCP connections) as the final fallback detection points -->

## Step 10 — Implement the detection(s).

Once you've applied the model to your environment, you hopefully will have found a solid detection strategy that works for your telemetry and environmental noise. Now it's time to write and deploy your detection queries. At this point, don't anguish over what you can't detect. Remember that we're building a mesh of detections that, in the aggregate, has a high likelihood of detecting an adversary somewhere on their path from initial access to impact. Just document your known blind spots, and make note of anything that would allow you to build a better detection in the future: maybe the ability to set a SACL, or enabling a particular log in Windows.

## Repeat!

At this point, you've analyzed the target attack technique, documented your results, built a strategy, and implemented it with detections. Now you select a new technique and start over. Technique by technique, your mesh will fill in, your attack surface coverage will grow, and the probability that an attacker will slip by undetected will shrink!

## Thoughts?

Thanks for reading! I hope you found something useful. If you have any thoughts to add, post a comment below!

---

**Tags:** Threat Detection, Detection Engineering, Detection Data Model, Technique Modeling, Cybersecurity