# LinkedIn Post — My Recipe App

---

My wife has this habit of screenshotting recipes from Instagram and then spending 10 minutes scrolling through her camera roll trying to find "that one pasta dish" while dinner is supposed to be happening.

So I did what any reasonable husband would do — I over-engineered a solution. 😅

Built her a recipe app called **My Recipes**. Nothing fancy on the surface: add recipes, organize them into collections, search by whatever random ingredient we have in the fridge. Works on her phone because that's where she actually cooks.

But of course I couldn't just throw it on a Raspberry Pi and call it a day. It had to be:
- Containerized (Docker)
- Running on our homelab Kubernetes cluster
- HTTPS-enabled with proper TLS certificates
- Backed up automatically every night
- Exportable to JSON so she owns her data

The stack is Flask + SQLAlchemy, SQLite with persistent volumes, Traefik for ingress, and cert-manager handling TLS. All living in a `my-recipe` namespace like a good little production workload.

It's hosted at `https://recipe.lab`. She uses it. She actually uses it. That single fact makes it the most successful deployment I've ever shipped.

Here's the thing I've learned: you can build microservices for thousands of users, but there's something special about building something for *one* person and watching it fit perfectly into their day.

#Flask #Python #Kubernetes #Homelab #SideProject #DevOps #WebDevelopment
