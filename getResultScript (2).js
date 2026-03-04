fetch('https://iiitd.nurecampus.com/NURE/spGetStudentLevels.action', {
  credentials: 'include',  // send cookies/session
  headers: {
    'Accept': 'application/json',
  },
})
.then(res => res.json())
.then(levels => {
  // Extract all level.id values
  const levelIds = levels.map(l => l.level.id);
  console.log('Available level IDs:', levelIds);

  // Use the first level id (e.g. latest semester) for marksheet download
  const levelId = levelIds[0];

  return fetch(`https://iiitd.nurecampus.com/NURE/downloadTermWiseMarksheet.action?&level.id=${levelId}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/pdf',
    },
    credentials: 'include'
  });
})
.then(response => {
  if (!response.ok) throw new Error(`Failed to download marksheet: ${response.status}`);

  return response.blob();
})
.then(blob => {
  // Trigger PDF download in browser
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'marksheet.pdf';
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
})
.catch(console.error);

