import React, { useState, useRef } from "react";
import "../assets/css/userentry.css"
const EntryForm = () => {
    const [fileNames, setFileNames] = useState("No files selected");
    const fileInputRef = useRef(null);

    const handleFileChange = (e) => {
        const files = e.target.files;
        if (files.length === 0) {
        setFileNames("No files selected");
        } else if (files.length === 1) {
        setFileNames(files[0].name);
        } else {
        setFileNames(`${files.length} files selected`);
        }
    };

    const handleButtonClick = () => {
        fileInputRef.current.click();
    };

    return (
        <div className="form-wrapper">
            <h2 className="form-label"> Product Content Generation</h2>
            <form>
                <input className="txt-entry" type="text" name="artistName" placeholder="Enter Artisan Name... " required/>
                <input className="txt-entry" name="artTitle" type="text" placeholder="Enter Art Title..." required/>
                <select name="artistType" required>
                    <option value="default">Select Art Type</option>
                    <option value="art1">Art 1</option>
                    <option value="art2">Art 2</option>
                    <option value="auto">Auto</option>
                </select>
                
                <textarea className="txt-entry" name="artdescription" rows="2" cols="20" placeholder="Artisan Notes.."></textarea>
                <input
                    className="txt-entry"
                    type="file"
                    id="attachments"
                    name="attachments"
                    multiple
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    style={{ display: "none" }}
                />
                <button id="file-select"type="button" onClick={handleButtonClick}>
                    Choose Files
                </button>
                <label className="file-input-label" htmlFor="attachments">
                    {fileNames}
                </label>
                <button className="submit-button" type="submit">Submit</button>
            </form>
        </div>
    )
}
export default EntryForm;