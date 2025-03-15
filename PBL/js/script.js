document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('nav ul');

    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('showing');
    });

    // Example of dynamically loading hackathon details
    const hackathons = [
        {
            title: 'Hackathons',
            details: 'Participate in thrilling hackathons and showcase your skills.',
            link: '#'
        },
        {
            title: 'Coding Resources',
            details: 'Access a wealth of coding resources to sharpen your skills.',
            link: '#'
        },
        {
            title: 'Challenges',
            details: 'Take on coding challenges to test and improve your abilities.',
            link: '#'
        }
    ];

    function loadHackathons() {
        const hackathonList = document.querySelector('.hackathon-list');
        hackathonList.innerHTML = ''; // Clear existing content

        hackathons.forEach(hackathon => {
            const hackathonItem = document.createElement('div');
            hackathonItem.classList.add('hackathon-item');

            const hackathonTitle = document.createElement('h3');
            hackathonTitle.textContent = hackathon.title;

            const hackathonDetails = document.createElement('p');
            hackathonDetails.textContent = hackathon.details;

            const hackathonLink = document.createElement('a');
            hackathonLink.href = hackathon.link;
            hackathonLink.classList.add('btn', 'btn-secondary');
            hackathonLink.textContent = 'Learn More';

            hackathonItem.appendChild(hackathonTitle);
            hackathonItem.appendChild(hackathonDetails);
            hackathonItem.appendChild(hackathonLink);

            hackathonList.appendChild(hackathonItem);
        });
    }

    // Load hackathons on page load
    loadHackathons();
});
