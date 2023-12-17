import React from 'react';
import './Contact.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEnvelope, faPhone } from '@fortawesome/free-solid-svg-icons';
import { faGithub, faLinkedin } from '@fortawesome/free-brands-svg-icons';
import SectionTitle from '../../components/SectionTitle';

const Contact = () => {
  return (
    <div id="contact" className="section">
      <SectionTitle title="Contact information" />

      <p>
        Please reach out to me for any questions or comments on my work, or if you'd just like to say hi.
      </p>

      <div className="contact-item">
        <FontAwesomeIcon icon={faEnvelope} className="icon" />
        <a href="mailto:jasperdeasey@gmail.com">jasperdeasey@gmail.com</a>
      </div>

      <div className="contact-item">
        <FontAwesomeIcon icon={faGithub} className="icon" />
        <a href="https://github.com/jasperdeasey" target="_blank" rel="noopener noreferrer">github.com/jasperdeasey</a>
      </div>

      <div className="contact-item">
        <FontAwesomeIcon icon={faLinkedin} className="icon" />
        <a href="https://linkedin.com/in/jasperdeasey" target="_blank" rel="noopener noreferrer">linkedin.com/in/jasperdeasey</a>
      </div>
    </div>
  );
};

export default Contact;
