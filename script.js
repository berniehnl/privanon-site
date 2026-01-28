// Privanon Website Scripts

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            mobileMenuBtn.classList.remove('active');
        });
    });

    // Navbar background on scroll
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(10, 15, 26, 0.98)';
        } else {
            navbar.style.background = 'rgba(10, 15, 26, 0.9)';
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '';  // Clear inline style so animation can work
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.solution-card, .tech-point, .value-card').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });

    // Form submission handler
    const contactForm = document.querySelector('.contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Collect form data
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());

            // Here you would typically send to a backend
            // For now, show a success message
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;

            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;

            // Simulate sending (replace with actual API call)
            setTimeout(() => {
                submitBtn.textContent = 'Message Sent!';
                submitBtn.style.background = '#10b981';

                // Reset form
                this.reset();

                // Reset button after delay
                setTimeout(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.style.background = '';
                    submitBtn.disabled = false;
                }, 3000);
            }, 1000);
        });
    }

    // Add tech diagram animation
    const techDiagram = document.querySelector('.tech-diagram');

    if (techDiagram) {
        const rings = techDiagram.querySelectorAll('.diagram-ring');

        rings.forEach((ring, index) => {
            ring.style.animation = `pulse ${3 + index}s ease-in-out infinite`;
        });
    }
});

// Add CSS for mobile menu and animations
const style = document.createElement('style');
style.textContent = `
    /* Mobile Menu Styles */
    @media (max-width: 768px) {
        .nav-links {
            position: fixed;
            top: 70px;
            left: 0;
            right: 0;
            background: rgba(10, 15, 26, 0.98);
            flex-direction: column;
            padding: 2rem;
            gap: 1.5rem;
            border-bottom: 1px solid var(--color-border);
            transform: translateY(-100%);
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }

        .nav-links.active {
            display: flex;
            transform: translateY(0);
            opacity: 1;
            visibility: visible;
        }

        .nav-cta {
            width: 100%;
            text-align: center;
        }

        .mobile-menu-btn.active span:nth-child(1) {
            transform: rotate(45deg) translate(5px, 5px);
        }

        .mobile-menu-btn.active span:nth-child(2) {
            opacity: 0;
        }

        .mobile-menu-btn.active span:nth-child(3) {
            transform: rotate(-45deg) translate(7px, -6px);
        }
    }

    /* Pulse Animation for Tech Diagram */
    @keyframes pulse {
        0%, 100% {
            opacity: 0.3;
            transform: translate(-50%, -50%) scale(1);
        }
        50% {
            opacity: 0.6;
            transform: translate(-50%, -50%) scale(1.02);
        }
    }

    /* Animation delay for staggered effects */
    .solution-card:nth-child(1) { animation-delay: 0.1s; }
    .solution-card:nth-child(2) { animation-delay: 0.2s; }
    .solution-card:nth-child(3) { animation-delay: 0.3s; }

    .tech-point:nth-child(1) { animation-delay: 0.1s; }
    .tech-point:nth-child(2) { animation-delay: 0.2s; }
    .tech-point:nth-child(3) { animation-delay: 0.3s; }

    .value-card:nth-child(1) { animation-delay: 0.1s; }
    .value-card:nth-child(2) { animation-delay: 0.2s; }
    .value-card:nth-child(3) { animation-delay: 0.3s; }
`;
document.head.appendChild(style);
