// Mevcut öğrencileri saklamak için bir liste
let students = [
    { id: '1', fullName: 'Ali Yılmaz', tcNo: '12345678901', birthday: { day: 10, month: 5, year: 2008 }, address: 'İstanbul', school: 'Okul 1', branch: 'A', score: 85 },
    { id: '2', fullName: 'Ayşe Demir', tcNo: '98765432101', birthday: { day: 20, month: 3, year: 2009 }, address: 'Ankara', school: 'Okul 2', branch: 'B', score: 92 }
];

// Başvuru yapan öğrencileri saklamak için bir liste (örnek veri)
let applications = [
    { id: '1', fullName: 'Ali Yılmaz', tcNo: '12345678901', birthday: { day: 10, month: 5, year: 2008 }, address: 'İstanbul', school: '', branch: '', score: 85 },
    { id: '2', fullName: 'Ayşe Demir', tcNo: '98765432101', birthday: { day: 20, month: 3, year: 2009 }, address: 'Ankara', school: '', branch: '', score: 92 }
];

// Öğrencileri gösterme işlevi
function showStudents() {
    document.getElementById('welcome-message').style.display = 'none'; // Karşılama mesajını gizle
    document.getElementById('students').style.display = 'block'; // Öğrenciler içeriğini göster
    document.getElementById('applications').style.display = 'none'; // Başvurular içeriğini gizle
    displayStudents(); // Öğrenci listesini güncelle
}

// Başvuruları gösterme işlevi
function showApplications() {
    document.getElementById('welcome-message').style.display = 'none'; // Karşılama mesajını gizle
    document.getElementById('students').style.display = 'none'; // Öğrenciler içeriğini gizle
    document.getElementById('applications').style.display = 'block'; // Başvurular içeriğini göster
    displayApplications(); // Başvuru listesini güncelle
}

// Öğrencileri listeleme işlevi
function displayStudents() {
    const studentTableBody = document.getElementById('student-table-body');
    studentTableBody.innerHTML = ''; // Mevcut içeriği temizle

    students.forEach((student, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${student.id}</td>
            <td>${student.fullName}</td>
            <td>${student.tcNo}</td>
            <td>${student.birthday.day}/${student.birthday.month}/${student.birthday.year}</td>
            <td>${student.address}</td>
            <td>${student.school}</td>
            <td>${student.branch}</td>
            <td>
                <button onclick="editStudent(${index})">Düzenle</button>
                <button onclick="deleteStudent(${index})">Sil</button>
            </td>
        `;
        studentTableBody.appendChild(row);
    });
}

// Başvuru yapan öğrencileri listeleme işlevi
function displayApplications() {
    const applicationTableBody = document.getElementById('application-table-body');
    applicationTableBody.innerHTML = ''; // Mevcut içeriği temizle

    // Başvuruları puanlarına göre sıralama (büyükten küçüğe)
    applications.sort((a, b) => b.score - a.score);

    applications.forEach((student) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${student.id}</td>
            <td>${student.fullName}</td>
            <td>${student.tcNo}</td>
            <td>${student.birthday.day}/${student.birthday.month}/${student.birthday.year}</td>
            <td>${student.address}</td>
            <td>${student.school || ''}</td>
            <td>${student.branch || ''}</td>
            <td>${student.score}</td>
            <td>
                <button onclick="selectStudent('${student.id}')">Seç</button>
            </td>
        `;
        applicationTableBody.appendChild(row);
    });
}

// Öğrenciyi düzenleme işlevi
function editStudent(index) {
    const student = students[index];
    document.getElementById('student-id').value = student.id;
    document.getElementById('full-name').value = student.fullName;
    document.getElementById('tc-no').value = student.tcNo;
    document.getElementById('birth-day').value = student.birthday.day;
    document.getElementById('birth-month').value = student.birthday.month;
    document.getElementById('birth-year').value = student.birthday.year;
    document.getElementById('address').value = student.address;
    document.getElementById('school').value = student.school;
    document.getElementById('branch').value = student.branch;

    document.getElementById('add-student').innerText = 'Bilgileri Güncelle'; // Buton metnini değiştir
}

// Öğrenciyi silme işlevi
function deleteStudent(index) {
    students.splice(index, 1); // Öğrenciyi diziden kaldır
    displayStudents(); // Öğrenci listesini güncelle
}

// Başvuruyu onaylama işlevi
function approveApplication() {
    const selectedStudentId = document.getElementById('application-id').value;
    const school = document.getElementById('application-school').value;
    const branch = document.getElementById('application-branch').value;

    const studentIndex = applications.findIndex(student => student.id === selectedStudentId);
    if (studentIndex >= 0) {
        applications[studentIndex].school = school;
        applications[studentIndex].branch = branch;
        displayApplications(); // Başvuru listesini güncelle
    } else {
        alert('Öğrenci bulunamadı.');
    }
}

// Öğrenciyi başvuru formuna seçme işlevi
function selectStudent(studentId) {
    const student = applications.find(student => student.id === studentId);
    if (student) {
        document.getElementById('application-id').value = student.id;
        document.getElementById('application-name').value = student.fullName;
        document.getElementById('application-tc').value = student.tcNo;
        document.getElementById('application-birth-day').value = student.birthday.day;
        document.getElementById('application-birth-month').value = student.birthday.month;
        document.getElementById('application-birth-year').value = student.birthday.year;
        document.getElementById('application-address').value = student.address;
        document.getElementById('application-school').value = student.school || '';
        document.getElementById('application-branch').value = student.branch || '';
    }
}

// Tarih seçim kutularını doldurma işlevi
function populateDateSelectors() {
    const days = document.getElementById('birth-day');
    const months = document.getElementById('birth-month');
    const years = document.getElementById('birth-year');

    for (let i = 1; i <= 31; i++) {
        days.add(new Option(i, i));
    }

    for (let i = 1; i <= 12; i++) {
        months.add(new Option(i, i));
    }

    for (let i = 1900; i <= new Date().getFullYear(); i++) {
        years.add(new Option(i, i));
    }
}

// Sayfa yüklendiğinde tarih seçeneklerini doldur
document.addEventListener('DOMContentLoaded', populateDateSelectors);
