gsap.from(".slide", {
    duration: 0.2,
    x: 70,
    opacity: 0
});

gsap.from(".slide-slow", {
    duration: 0.3,
    x: 70,
    opacity: 0
});

gsap.from(".show", {
    duration: 0.3,
    y: 70,
    opacity: 0
});

tl = gsap.timeline();

tl.from(".articles", {
    duration: 0.5,
    opacity: 0,
    y: 25,
    stagger: 0.1
});
tl.addLabel("circlesOutro", "-=1");