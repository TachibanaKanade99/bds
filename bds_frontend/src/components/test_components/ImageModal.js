import React, { Component } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

class ImageModal extends Component {
    constructor(props) {
        super(props);
        this.state = {
            modal: false,
        }
        this.toggleModal = this.toggleModal.bind(this);
    }

    toggleModal = () => {
        this.setState({ setModal: !this.state.modal})
    }

    render() {
        return (
            
        )
    }
}