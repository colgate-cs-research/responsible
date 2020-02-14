from model_build import get_ngrams

text1 = "We at Cogent support Net Neutrality – no blocking or throttling of traffic, no paid prioritization of traffic, full access to all lawful content on the Internet, and free flowing interconnection among Internet providers."
text2 = "Recently, the Federal Communications Commission rescinded its rules enforcing Net Neutrality. We think that is bad for Internet users and for the Internet. Cogent practices net neutrality. We do not prioritize packet transmissions on the basis of the content of the packet, the customer or network that is the source of the packet, or the customer or network that is the recipient of the packet. Where there are network problems such as congestion at interconnection points or fiber cuts we implement network management tools to minimize harm to the users of our network."
text3 = "It is Cogent's belief that both the customer and the Internet as a whole are best served if the application layer remains independent from the network. Innovation in the development of new applications is fueled by the individual's ability to reach as many people as possible without regard to complicated gating factors such as tiered pricing or bandwidth structures used by legacy service providers. Applications proliferate in a free market economy which is the Internet today."

text = [text1, text2, text3]

print(get_ngrams(text))