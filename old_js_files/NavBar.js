import React from 'react'
import { useNavigate } from 'react-router-dom';
import '../componentStyles/NavBarStyles.css';
import LogoutModal from '../front-end/src/components/LogoutModal';
import CloseAccountModal from '../front-end/src/components/CloseAccountModal';
import CancelAutomaticPayments from '../front-end/src/components/CancelAutomaticPayments';

function NavBar() {
    const navigate = useNavigate();


    return (
        <div className='row'>
            {/* <!-- Responsive navbar--> */}
            <div className='col-md-12'>
                <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                    <div className="container px-5">
                        <img
                            src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/lotus.webp"
                            style={{ width: '85px' }}
                            alt="logo"
                            id="logo"
                        />
                        <a className="navbar-brand" id="home" onClick={() => navigate('/home')}>Hoken</a>
                        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"><span className="navbar-toggler-icon"></span></button>
                        <div className="collapse navbar-collapse" id="navbarSupportedContent">
                            <ul className="navbar-nav ms-auto mb-lg-0 my-2">
                                <li className="nav-item my-2"><button type="button" className="nav-link btn btn-outline-secondary nav-bar-bttn" onClick={() => navigate('/atmSearch')}><i className="bi bi-search me-2"></i>ATM Search</button></li>
                                <li className="nav-item my-2">
                                    <CancelAutomaticPayments/>
                                </li>
                                <li className="nav-item my-2">
                                    <CloseAccountModal/>
                                </li>
                                <li className="nav-item my-2">
                                    <LogoutModal />
                                </li>
                            </ul>
                        </div>
                    </div>
                </nav>
            </div>
        </div>
    )
}

export default NavBar;