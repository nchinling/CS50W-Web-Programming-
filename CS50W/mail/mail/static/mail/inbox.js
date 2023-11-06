document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', send_email)
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_email(id){
  console.log('I am inside view_email of id:' + id)
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        // Print email
        console.log(email);
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
        document.querySelector('#email-view').style.display = 'block';
        document.querySelector('#email-view').innerHTML = `

          <h1>${email.subject}</h1>
          <h6>${email.sender} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <i>${email.timestamp}</i></h6>
          <b>to: </b> ${email.recipients}
          </br>
          <p>${email.body} </p>
        
        `
        if(!email.read){
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })
        }

      const archive_button = document.createElement('button');
      archive_button.innerHTML = email.archived? "Unarchive" : "Archive";
      archive_button.addEventListener('click', function() {
          console.log('This button has been clicked!')
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: !email.archived
            })
          })
          .then(()=>{load_mailbox('inbox')})
      });
      document.querySelector('#email-view').append(archive_button);
    
      const reply_button = document.createElement('button');
      reply_button.innerHTML = "Reply";
      reply_button.addEventListener('click', function() {
        compose_email();
        document.querySelector('#compose-recipients').value = email.sender;
        var subject = email.subject;
        if (!subject.startsWith("Re:")) {
          subject = "Re: " + subject;
        }
        
        document.querySelector('#compose-subject').value = subject;
        document.querySelector('#compose-body').value = 
        `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
      });
      document.querySelector('#email-view').append(reply_button);
      
    });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      emails.forEach(email => {

        
        const element = document.createElement('div');
        element.innerHTML = `
          <p><b>Sender:</b> ${email.sender}&nbsp; <b>Subject:</b> ${email.subject}&nbsp;&nbsp; <i>${email.timestamp} </i></p>

        `;

        element.className = email.read? 'read': 'unread';
        element.addEventListener('click', function() {
            console.log('This element has been clicked!')
            view_email(email.id)
        });
        document.querySelector('#emails-view').append(element);

      })

      // ... do something else with emails ...
  });


}

function send_email(event){
  event.preventDefault();
  console.info('I am inside send_email')

  const recipients = document.querySelector('#compose-recipients').value;
  const subject =document.querySelector('#compose-subject').value;
  const body =document.querySelector('#compose-body').value;

  //post email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients:  recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  });

}

