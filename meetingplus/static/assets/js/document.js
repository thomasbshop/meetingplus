function showDocumentFunction(documentId){
    const viewerElement = document.getElementById('viewer');
    // var documentId = 15;
    let annotManager = null;
    const DOCUMENT_ID = documentId;
    const protocol = window.location.protocol;
    const port = window.location.port;
    const hostName = window.location.hostname;
    console.log('{{ document_id }}')
    const url = `ws://${hostName}:${port}/ws/meeting/document/${documentId}/`;
    const connection = new WebSocket(url);
    console.log(connection);
    const nameList = ['Andy', 'Andrew', 'Logan', 'Justin', 'Matt', 'Sardor', 'Zhijie', 'James', 'Kristian', 'Mary', 'Patricia', 'Jennifer', 'Linda', 'David', 'Joseph', 'Thomas', 'Naman', 'Nancy', 'Sandra'];
    const serializer = new XMLSerializer();

    connection.onerror = error => {
        console.warn(`Error from WebSocket: ${error}`);
    }
    console.log(url, `http://${hostName}:${port}{{ document_path }}`)
    connection.addEventListener("open", function(e){
      console.log("Public Public ChatSocket OPEN")
          // join chat room
          if("{{request.user.is_authenticated}}"){
              connection.send(JSON.stringify({
                  "command": "join",
                  "documentId": documentId
              }));
          }
      })

    WebViewer({
    path: 'static/lib', // path to the PDFTron 'lib' folder
    initialDoc: `http://${hostName}:${port}{{ document_path }}`,
    // initialDoc: 'https://pdftron.s3.amazonaws.com/downloads/pl/webviewer-demo.pdf',
    documentXFDFRetriever: async () => {
        const rows = await loadXfdfStrings(DOCUMENT_ID);
        return JSON.parse(rows).map(row => row.xfdfString);
    },
    }, viewerElement).then( instance => {

    // Instance is ready here
    console.log(instance);
    instance.openElements(['leftPanel']);
    annotManager = instance.docViewer.getAnnotationManager();
    // Assign a random name to client
    annotManager.setCurrentUser(nameList[Math.floor(Math.random()*nameList.length)]);
    annotManager.on('annotationChanged', async e => {
        // If annotation change is from import, return
        if (e.imported) {
        return;
        }

        const xfdfString = await annotManager.exportAnnotCommand();
        // Parse xfdfString to separate multiple annotation changes to individual annotation change
        const parser = new DOMParser();
        const commandData = parser.parseFromString(xfdfString, 'text/xml');
        const addedAnnots = commandData.getElementsByTagName('add')[0];
        const modifiedAnnots = commandData.getElementsByTagName('modify')[0];
        const deletedAnnots = commandData.getElementsByTagName('delete')[0];

        // List of added annotations
        addedAnnots.childNodes.forEach((child) => {
        sendAnnotationChange(child, 'add');
        });

        // List of modified annotations
        modifiedAnnots.childNodes.forEach((child) => {
        sendAnnotationChange(child, 'modify');
        });
        
        // List of deleted annotations
        deletedAnnots.childNodes.forEach((child) => {
        sendAnnotationChange(child, 'delete');
        });
    });

    connection.onmessage = async (message) => {
        const annotation = JSON.parse(message.data);
        const annotations = await annotManager.importAnnotCommand(annotation.xfdfString);
        await annotManager.drawAnnotationsFromList(annotations);
        }
    });

    const loadXfdfStrings = (documentId) => {
    return new Promise((resolve, reject) => {
        fetch(`/server/annotationHandler.js?documentId=${documentId}`, {
        method: 'GET',
        }).then((res) => {
        if (res.status < 400) {
            res.text().then(xfdfStrings => {
            resolve(xfdfStrings);
            });
        } else {
            reject(res);
        }
        });
    });
    };


    // wrapper function to convert xfdf fragments to full xfdf strings
    const convertToXfdf = (changedAnnotation, action) => {
    let xfdfString = `<?xml version="1.0" encoding="UTF-8" ?><xfdf xmlns="http://ns.adobe.com/xfdf/" xml:space="preserve"><fields />`;
    if (action === 'add') {
        xfdfString += `<add>${changedAnnotation}</add><modify /><delete />`;
    } else if (action === 'modify') {
        xfdfString += `<add /><modify>${changedAnnotation}</modify><delete />`;
    } else if (action === 'delete') {
        xfdfString += `<add /><modify /><delete>${changedAnnotation}</delete>`;
    }
    xfdfString += `</xfdf>`;
    return xfdfString;
    }

    // helper function to send annotation changes to WebSocket server
    const sendAnnotationChange = (annotation, action) => {
        if (annotation.nodeType !== annotation.TEXT_NODE) {
            const annotationString = serializer.serializeToString(annotation);
            connection.send(JSON.stringify({
            command: "send",
            documentId: DOCUMENT_ID,
            annotationId: annotation.getAttribute('name'),
            xfdfString: convertToXfdf(annotationString, action)
            }));
        }
    }
}