import { createBrowserRouter, createRoutesFromElements, Route } from "react-router-dom";
import Login from "@/pages/auth/Login";


export const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      {/* Auth routes */}
      <Route path="/" element={<Login />} />
      {/* <Route path="/register" element={<Register />} /> */}

      {/* Client routes */}
      {/* <Route path="client" element={<ProtectedCustomerRoute />}>
        <Route element={<ClientLayout />}>
          <Route index element={<CustomerHome />} />
          <Route path="products" element={<Products />} />
        </Route>
      </Route> */}

      {/* Admin routes */}
      {/* <Route path="admin" element={<ProtectedAdminRoute />}>
        <Route element={<AdminLayout />}>
          <Route index element={<Dashboard />} />

          <Route path="products">
            <Route index element={<ViewProducts />} />
            <Route path="add" element={<AddProduct />} />
            <Route path="archive" element={<ArchiveProducts />} />
            <Route path=":id" element={<EditProduct />} />
          </Route>

          <Route path="brands">
            <Route index element={<ViewBrands />} />
            <Route path="add" element={<AddBrand />} />
            <Route path="archive" element={<ArchiveBrands />} />
            <Route path=":id" element={<EditBrand />} />
          </Route>

          <Route path="users">
            <Route index element={<ViewUsers />} />
            <Route path="archive" element={<ArchiveUsers />} />
            <Route path=":id" element={<EditUser />} />
          </Route>

          <Route path="orders">
            <Route index element={<ViewOrders />} />
            <Route path="archive" element={<ArchiveOrders />} />
            <Route path=":id" element={<DetailsOrder />} />
          </Route>

          <Route path="categories">
            <Route index element={<ViewCategories />} />
            <Route path="add" element={<AddCategory />} />
            <Route path="archive" element={<ArchiveCategories />} />
            <Route path=":id" element={<EditCategory />} />
          </Route>

          <Route path="pc-builds">
            <Route index element={<ViewPCBuilds />} />
            <Route path="add" element={<AddPCBuild />} />
            <Route path="archive" element={<ArchivePCBuilds />} />
            <Route path=":id" element={<DetailsPCBuild />} />
          </Route>

          <Route path="account" element={<AccountAdmin />} />
        </Route>
      </Route>

      <Route path="*" element={<NotFound />} /> */}
    </>
  )
);
