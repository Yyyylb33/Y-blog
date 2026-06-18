// =========================

// 页面加载完成

// =========================

document.addEventListener("DOMContentLoaded", function () {

    console.log("Blog System Loaded");

    initLikeButton();

    initDeleteConfirm();

});

// =========================

// 点赞功能

// =========================

function likePost(postId) {

    fetch(`/like/${postId}`)

        .then(response => response.json())

        .then(data => {

            // 未登录

            if (data.status === "login") {

                alert("请先登录");

                window.location.href = "/login";

                return;

            }

            let countElement =

                document.getElementById("likeCount");

            if (countElement) {

                countElement.innerText = data.count;

            }

            let button =

                document.getElementById("likeBtn");

            if (button) {

                if (data.liked) {

                    button.innerHTML = "❤️ 已点赞";

                    button.classList.add("liked");

                } else {

                    button.innerHTML = "🤍 点赞";

                    button.classList.remove("liked");

                }

            }

        })

        .catch(error => {

            console.error(error);

            alert("点赞失败");

        });

}

// =========================

// 初始化点赞按钮

// =========================

function initLikeButton() {

    const btn =

        document.getElementById("likeBtn");

    if (!btn) return;

    btn.addEventListener("mouseenter", function () {

        btn.style.transform = "scale(1.05)";

    });

    btn.addEventListener("mouseleave", function () {

        btn.style.transform = "scale(1)";

    });

}

// =========================

// 删除确认

// =========================

function initDeleteConfirm() {

    const deleteButtons =

        document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(button => {

        button.addEventListener("click", function (e) {

            const result =

                confirm("确定删除这篇文章吗？");

            if (!result) {

                e.preventDefault();

            }

        });

    });

}

// =========================

// 评论字数统计

// =========================

function updateCommentCount() {

    const textarea =

        document.getElementById("commentText");

    const counter =

        document.getElementById("commentCount");

    if (!textarea || !counter) return;

    counter.innerText =

        textarea.value.length;

}

// =========================

// 搜索框回车

// =========================

function searchSubmit(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        document.getElementById(

            "searchForm"

        ).submit();

    }

}

// =========================

// 返回顶部

// =========================

function scrollTopSmooth() {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

}

// =========================

// 自动显示返回顶部按钮

// =========================

window.addEventListener("scroll", function () {

    const btn =

        document.getElementById("topBtn");

    if (!btn) return;

    if (window.scrollY > 300) {

        btn.style.display = "block";

    } else {

        btn.style.display = "none";

    }

});

// =========================

// Markdown编辑器预览

// =========================

function previewMarkdown() {

    const input =

        document.getElementById("markdownInput");

    const preview =

        document.getElementById("markdownPreview");

    if (!input || !preview) return;

    preview.innerText =

        input.value;

}

// =========================

// Toast提示

// =========================

function showToast(message) {

    let toast =

        document.createElement("div");

    toast.className =

        "toast-message";

    toast.innerText =

        message;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.remove();

    }, 3000);

}

// =========================

// 图片预览

// =========================

function previewImage(input) {

    const preview =

        document.getElementById("imagePreview");

    if (!preview) return;

    const file =

        input.files[0];

    if (!file) return;

    const reader =

        new FileReader();

    reader.onload = function (e) {

        preview.src =

            e.target.result;

        preview.style.display =

            "block";

    };

    reader.readAsDataURL(file);

}
