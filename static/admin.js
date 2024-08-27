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

// Mevcut kreşleri saklamak için bir liste
let nurseries = [
    { id: '1', name: 'Kreş 1', branchCount: 5, capacity: 50 },
    { id: '2', name: 'Kreş 2', branchCount: 3, capacity: 40 }
];

// Şubeleri saklamak için bir liste (örnek veri)
let branches = [
    { id: '1', name: 'Şube 1', nursery: 'Kreş 1', capacity: 20, teachers: ['Öğretmen 1'] },
    { id: '2', name: 'Şube 2', nursery: 'Kreş 2', capacity: 15, teachers: ['Öğretmen 3'] }
];

// Bölümleri gizleme işlevi
function hideAllSections() {
    const sections = document.querySelectorAll('.content > div');
    sections.forEach(section => section.classList.add('hidden'));
}

// Öğrencileri gösterme işlevi
function showStudents() {
    hideAllSections();
    document.getElementById('students').classList.remove('hidden');
    displayStudents();
}

// Başvuruları gösterme işlevi
function showApplications() {
    hideAllSections();
    document.getElementById('applications').classList.remove('hidden');
    displayApplications();
}

// Kreşleri gösterme işlevi
function showNurseries() {
    hideAllSections();
    document.getElementById('nurseries').classList.remove('hidden');
    displayNurseries();
}

// Şubeleri gösterme işlevi
function showBranches() {
    hideAllSections();
    document.getElementById('branches').classList.remove('hidden');
    displayBranches();
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

// Kreşleri listeleme işlevi
function displayNurseries() {
    const nurseryTableBody = document.getElementById('nursery-table-body');
    nurseryTableBody.innerHTML = '';

    nurseries.forEach((nursery, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${nursery.id}</td>
            <td>${nursery.name}</td>
            <td>${nursery.branchCount}</td>
            <td>${nursery.capacity}</td>
            <td>
                <button onclick="editNursery(${index})">Düzenle</button>
                <button onclick="deleteNursery(${index})">Sil</button>
            </td>
        `;
        nurseryTableBody.appendChild(row);
    });
}

// Şubeleri listeleme işlevi
function displayBranches() {
    const branchTableBody = document.getElementById('branch-table-body');
    branchTableBody.innerHTML = '';

    branches.forEach((branch, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${branch.id}</td>
            <td>${branch.name}</td>
            <td>${branch.nursery}</td>
            <td>${branch.capacity}</td>
            <td>${branch.teachers.join(', ')}</td>
            <td>
                <button onclick="editBranch(${index})">Düzenle</button>
                <button onclick="deleteBranch(${index})">Sil</button>
            </td>
        `;
        branchTableBody.appendChild(row);
    });
}

// TC No alanına sadece sayı girilmesini sağla ve 11 haneli olmasını kontrol et
document.getElementById('tc-no').addEventListener('input', function (e) {
    const value = e.target.value.replace(/\D/g, ''); // Sayı olmayan karakterleri kaldır
    e.target.value = value.slice(0, 11); // Maksimum 11 hane
});

// Gün, ay, yıl seçeneklerini oluşturma işlevi
function populateDateSelectors() {
    const daySelect = document.getElementById('birth-day');
    const monthSelect = document.getElementById('birth-month');
    const yearSelect = document.getElementById('birth-year');

    // Gün seçeneklerini doldur
    for (let i = 1; i <= 31; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        daySelect.appendChild(option);
    }

    // Ay seçeneklerini doldur
    for (let i = 1; i <= 12; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        monthSelect.appendChild(option);
    }

    // Yıl seçeneklerini doldur
    const currentYear = new Date().getFullYear();
    for (let i = currentYear; i >= currentYear - 30; i--) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        yearSelect.appendChild(option);
    }
}

// Öğrenci ekleme veya güncelleme işlevi
function addOrUpdateStudent() {
    const studentId = document.getElementById('student-id').value;
    const fullName = document.getElementById('full-name').value;
    const tcNo = document.getElementById('tc-no').value;
    const birthDay = document.getElementById('birth-day').value;
    const birthMonth = document.getElementById('birth-month').value;
    const birthYear = document.getElementById('birth-year').value;
    const address = document.getElementById('address').value;
    const school = document.getElementById('school').value;
    const branch = document.getElementById('branch').value;

    // Doğum tarihi seçilmediğinde boş değerleri işaretle
    if (!birthDay || !birthMonth || !birthYear) {
        alert('Lütfen doğum tarihini eksiksiz girin.');
        return;
    }

    const existingStudentIndex = students.findIndex(student => student.id === studentId);

    if (existingStudentIndex >= 0) {
        // Mevcut öğrenciyi güncelle
        students[existingStudentIndex] = { id: studentId, fullName, tcNo, birthday: { day: birthDay, month: birthMonth, year: birthYear }, address, school, branch };
        document.getElementById('add-student').innerText = 'Öğrenci Ekle';
    } else {
        // Yeni öğrenci ekle
        students.push({ id: studentId, fullName, tcNo, birthday: { day: birthDay, month: birthMonth, year: birthYear }, address, school, branch });
    }

    // Formu temizle
    document.getElementById('student-id').value = '';
    document.getElementById('full-name').value = '';
    document.getElementById('tc-no').value = '';
    document.getElementById('birth-day').value = '';
    document.getElementById('birth-month').value = '';
    document.getElementById('birth-year').value = '';
    document.getElementById('address').value = '';
    document.getElementById('school').value = 'Okul 1';
    document.getElementById('branch').value = 'A';

    displayStudents(); // Öğrenci listesini güncelle
}

// Öğrenci düzenleme işlevi
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

    document.getElementById('add-student').innerText = 'Öğrenciyi Güncelle'; // Buton metnini değiştir
}

// Öğrenci silme işlevi
function deleteStudent(index) {
    students.splice(index, 1); // Öğrenciyi diziden kaldır
    displayStudents(); // Öğrenci listesini güncelle
}

// Kreş ekleme veya güncelleme işlevi
function addOrUpdateNursery() {
    const nurseryId = document.getElementById('nursery-id').value;
    const nurseryName = document.getElementById('nursery-name').value;
    const branchCount = document.getElementById('nursery-branch-count').value;
    const capacity = document.getElementById('nursery-capacity').value;

    const existingNurseryIndex = nurseries.findIndex(nursery => nursery.id === nurseryId);

    if (existingNurseryIndex >= 0) {
        // Mevcut kreşi güncelle
        nurseries[existingNurseryIndex] = { id: nurseryId, name: nurseryName, branchCount, capacity };
        document.getElementById('add-nursery').innerText = 'Kreş Ekle';
    } else {
        // Yeni kreş ekle
        nurseries.push({ id: nurseryId, name: nurseryName, branchCount, capacity });
    }

    // Formu temizle
    document.getElementById('nursery-id').value = '';
    document.getElementById('nursery-name').value = '';
    document.getElementById('nursery-branch-count').value = '';
    document.getElementById('nursery-capacity').value = '';

    displayNurseries(); // Kreş listesini güncelle
}

// Kreşi düzenleme işlevi
function editNursery(index) {
    const nursery = nurseries[index];
    document.getElementById('nursery-id').value = nursery.id;
    document.getElementById('nursery-name').value = nursery.name;
    document.getElementById('nursery-branch-count').value = nursery.branchCount;
    document.getElementById('nursery-capacity').value = nursery.capacity;

    document.getElementById('add-nursery').innerText = 'Kreşi Güncelle'; // Buton metnini değiştir
}

// Kreşi silme işlevi
function deleteNursery(index) {
    nurseries.splice(index, 1); // Kreşi diziden kaldır
    displayNurseries(); // Kreş listesini güncelle
}

// Şube ekleme veya güncelleme işlevi
function addOrUpdateBranch() {
    const branchId = document.getElementById('branch-id').value;
    const branchName = document.getElementById('branch-name').value;
    const nursery = document.getElementById('branch-nursery').value;
    const capacity = document.getElementById('branch-capacity').value;
    const teachers = Array.from(document.querySelectorAll('#branch-teachers option:checked'), option => option.value);

    const existingBranchIndex = branches.findIndex(branch => branch.id === branchId);

    if (existingBranchIndex >= 0) {
        // Mevcut şubeyi güncelle
        branches[existingBranchIndex] = { id: branchId, name: branchName, nursery, capacity, teachers };
        document.getElementById('add-branch').innerText = 'Şube Ekle';
    } else {
        // Yeni şube ekle
        branches.push({ id: branchId, name: branchName, nursery, capacity, teachers });
    }

    // Formu temizle
    document.getElementById('branch-id').value = '';
    document.getElementById('branch-name').value = '';
    document.getElementById('branch-nursery').value = '';
    document.getElementById('branch-capacity').value = '';
    document.getElementById('branch-teachers').value = '';

    displayBranches(); // Şube listesini güncelle
}

// Şube düzenleme işlevi
function editBranch(index) {
    const branch = branches[index];
    document.getElementById('branch-id').value = branch.id;
    document.getElementById('branch-name').value = branch.name;
    document.getElementById('branch-nursery').value = branch.nursery;
    document.getElementById('branch-capacity').value = branch.capacity;
    document.getElementById('branch-teachers').value = branch.teachers;

    document.getElementById('add-branch').innerText = 'Şubeyi Güncelle'; // Buton metnini değiştir
}

// Şube silme işlevi
function deleteBranch(index) {
    branches.splice(index, 1); // Şubeyi diziden kaldır
    displayBranches(); // Şube listesini güncelle
}

// Sayfa yüklendiğinde tarih seçeneklerini doldur
document.addEventListener('DOMContentLoaded', populateDateSelectors);

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
