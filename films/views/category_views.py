from films.models import Category
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff



class CategoryCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'categories/category.html'
    fields = "__all__"
    permission_required = "category.add_category"

    def get_success_url(self):
        messages.success(self.request, "New category successfully added")
        return reverse_lazy("categories")



class CategoryListView(ListView):
    model = Category
    template_name = "categories/category_list.html"
    context_object_name = "categories"



class CategoryUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Category
    template_name = "categories/category.html"
    fields = "__all__"
    success_url = reverse_lazy("categories")
    permission_required = "categories.change_category"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Category data successfully changed")
        return super().form_valid(form)



class CategoryDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "categories/category_confirm_delete.html"

    def get_success_url(self):
        messages.error(self.request, "Category successfully deleted")
        return reverse_lazy("categories")