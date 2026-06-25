document$.subscribe(function () {
  mermaid.initialize({
    startOnLoad: false,
    theme: "default",
    securityLevel: "loose"
  });

  mermaid.run({
    querySelector: ".mermaid"
  });
});
