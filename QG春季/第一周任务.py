import json
import numpy as np
import math

with open('data(1).json','r') as f:
    data = json.load(f)

class coordsystem:
    def __init__(self,ori_axis,vectors):
        self.basis = np.array(ori_axis).T.astype(float)
        self.vectors = np.array(vectors).T.astype(float)

    def change_axis(self,target_basis):
        target_basis = np.array(target_basis).T.astype(float)

        transform_martix = np.linalg.inv(target_basis) @ self.basis
        self.vectors = transform_martix @ self.vectors

        #完成之后需要更新坐标系
        self.basis = target_basis

    def axis_projection(self):
        projection = []
        d,m = self.vectors.shape

        for i in range(m):
            vec = self.vectors[:,i]
            vec_projection = []
            for j in range(d):
                axis = self.basis[:,j]
                pro_len = np.dot(vec,axis)/np.dot(axis,axis)
                vec_projection.append(pro_len)
            projection.append(vec_projection)
        return projection

    def area(self):
        return abs(np.linalg.det(self.basis))

    def axis_angle(self):
        angles = []
        d,m = self.vectors.shape

        for i in range(m):
            vec = self.vectors[:,i]
            vec_angles = []
            norm_vec = np.linalg.norm(vec)#norm是用来计算向量长度的函数

            for j in range(d):
                axis = self.basis[:,j]
                norm_axis = np.linalg.norm(axis)

                if norm_vec == 0 or norm_axis == 0:
                    vec_angles.append(math.nan)
                else:
                    cos_end = np.dot(vec,axis)/(norm_axis*norm_axis)
                    #根据ai的提示，处理误差导致cos值超过-1和1的情况
                    cos_end_clipped = np.clip(cos_end,-1,1)
                    angle = math.acos(cos_end_clipped)
                    vec_angles.append(angle)
            angles.append(vec_angles)
        return angles

    def get_vectors_as_list(self):
        return self.vectors.T.tolist()
    def get_basis_as_list(self):
        return self.basis.T.tolist()

def process_json_file(filepath):
    with open(filepath,'r') as f:
        all_task_groups = json.load(f)

    all_results = {}

    for task_group in all_task_groups:
        group_name = task_group['group_name']
        print(f"\n{'='*50}")
        print(f"处理任务组：{group_name}")
        print(f"初始坐标系：{task_group['ori_axis']}")
        print(f"初始向量集：{task_group['vectors'][:3]}...")

        cs = coordsystem(task_group['ori_axis'],task_group['vectors'])

        group_results = []

        for idx,task in enumerate(task_group['tasks']):#enumerate函数的作用，返还两个值（下标索引，元素）
            task_type = task['type']
            print(f"  任务{idx+1}: {task_type}",end = "  ")#end的作用是会在末尾添加完指定元素之后就自动换行

            if task_type == 'change_axis':
                new_basis = task['obj_basis']
                transformed_vectors = cs.change_axis(new_basis)

                result = {
                    "new_basis": new_basis,
                    "transformed_vectors": transformed_vectors[:2]
                }
                print("坐标系已更新")

            elif task_type == 'axis_angle':
                angles = cs.axis_angle()
                result = {"angle_samples": angles[:2]}
                print("夹角计算完成")

            elif task_type == 'axis_projection':
                projection = cs.axis_projection()
                result = {"projection_samples": projection[:2]}
                print("投影计算完成")

            elif task_type == 'area':
                scaling = cs.area()
                result = {"area_scaling_factor": scaling}
                print(f"面积缩放倍速：{scaling:.4f}")

            group_results.append({task_type: result})

        final_state = {
            "final_basis": cs.get_basis_as_list(),
            "final_vectors": cs.get_vectors_as_list(),
            "group_result": group_results
        }
        all_results[group_name] = final_state


import json
import numpy as np
import math


class CoordinateSystem:

    def __init__(self, ori_axis, vectors):

        # 转换为NumPy数组，并转为列向量排列 (d, n) 和 (d, m)
        # d: 维度, n: 基向量数量, m: 向量数量
        self.basis = np.array(ori_axis).T.astype(float)  # 形状 (d, n)
        self.vectors = np.array(vectors).T.astype(float)  # 形状 (d, m)

        # 验证维度匹配
        if self.basis.shape[0] != self.vectors.shape[0]:
            raise ValueError("基向量与向量的维度不匹配。")

    def change_axis(self, new_basis):

        new_basis = np.array(new_basis).T.astype(float)

        # 检查新基向量矩阵是否可逆（即能否构成坐标系）
        if new_basis.shape[0] != new_basis.shape[1] or np.linalg.matrix_rank(new_basis) < new_basis.shape[0]:
            raise ValueError("提供的目标基向量无法构成一个有效的坐标系（非满秩或非方阵）。")

        # 核心变换公式: [新坐标] = inv(新基) * [当前基] * [旧坐标]
        # 注意：我们的 self.vectors 已经是 [旧坐标] 的列向量组合
        transform_matrix = np.linalg.inv(new_basis) @ self.basis
        self.vectors = transform_matrix @ self.vectors

        # 更新当前坐标系
        self.basis = new_basis

        return self.get_vectors_as_list()

    def axis_projection(self):
        projections = []
        d, m = self.vectors.shape

        for i in range(m):
            vec = self.vectors[:, i]
            vec_projections = []
            for j in range(d):
                axis = self.basis[:, j]
                # 投影长度 = (v·u) / (u·u)
                proj_len = np.dot(vec, axis) / np.dot(axis, axis)
                vec_projections.append(proj_len)
            projections.append(vec_projections)
        return projections

    def axis_angle(self):
        angles = []
        d, m = self.vectors.shape

        for i in range(m):
            vec = self.vectors[:, i]
            vec_angles = []
            norm_v = np.linalg.norm(vec)

            for j in range(d):
                axis = self.basis[:, j]
                norm_axis = np.linalg.norm(axis)

                if norm_v == 0 or norm_axis == 0:
                    vec_angles.append(math.nan)  # 零向量与轴的夹角未定义
                else:
                    cos_theta = np.dot(vec, axis) / (norm_v * norm_axis)
                    # 处理数值误差可能导致 |cos_theta| 略大于1的情况
                    cos_theta_clipped = np.clip(cos_theta, -1.0, 1.0)
                    angle = math.acos(cos_theta_clipped)
                    vec_angles.append(angle)
            angles.append(vec_angles)
        return angles

    def area(self):
        # 缩放倍数 = |det(当前基向量矩阵)|
        return abs(np.linalg.det(self.basis))

    def can_be_basis(self, basis_vectors):
        mat = np.array(basis_vectors)
        if mat.shape[0] != mat.shape[1]:
            return False, f"向量数量({mat.shape[0]})与维度({mat.shape[1]})不相等，无法构成基。"
        if np.linalg.matrix_rank(mat) < mat.shape[0]:
            return False, "向量线性相关，无法张成整个空间。"
        return True, "可以构成有效的坐标系。"

    def get_vectors_as_list(self):
        return self.vectors.T.tolist()

    def get_basis_as_list(self):
        return self.basis.T.tolist()


def process_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        all_task_groups = json.load(f)

    all_results = {}

    for task_group in all_task_groups:
        group_name = task_group['group_name']
        print(f"\n{'=' * 50}")
        print(f"处理任务组: {group_name}")
        print(f"初始坐标系: {task_group['ori_axis']}")
        print(f"初始向量: {task_group['vectors'][:3]}...")

        try:
            cs = CoordinateSystem(task_group['ori_axis'], task_group['vectors'])
        except ValueError as e:
            print(f"  初始化失败: {e}")
            all_results[group_name] = {"error": str(e)}
            continue

        group_results = []

        for idx, task in enumerate(task_group['tasks']):
            task_type = task['type']
            print(f"  任务{idx + 1}: {task_type}", end=" ")


            if task_type == 'change_axis':
                new_basis = task['obj_axis']
                # 任务4：判断目标坐标系是否有效
                is_valid, reason = cs.can_be_basis(new_basis)
                if not is_valid:
                    result = f"错误: 目标坐标系无效 - {reason}"
                    group_results.append({task_type: result})
                    print(f"- 目标坐标系无效，跳过")
                    continue

                transformed_vectors = cs.change_axis(new_basis)
                result = {
                    "new_basis": new_basis,
                     "transformed_vectors_sample": transformed_vectors[:2]  # 只存样本
                }
                print(f"- 坐标系已更新")

            elif task_type == 'axis_projection':
                projections = cs.axis_projection()
                result = {"projections_sample": projections[:2]}  # 只存样本
                print(f"- 投影计算完成")

            elif task_type == 'axis_angle':
                angles = cs.axis_angle()
                result = {"angles_sample": angles[:2]}  # 只存样本
                print(f"- 夹角计算完成")

            elif task_type == 'area':
                scaling = cs.area()
                result = {"area_scaling_factor": scaling}
                print(f"- 面积缩放倍数: {scaling:.4f}")

            else:
                result = f"错误: 未知任务类型 '{task_type}'"
                print(f"- 未知类型")

            group_results.append({task_type: result})

        final_state = {
            "final_basis": cs.get_basis_as_list(),
            "final_vectors": cs.get_vectors_as_list(),
            "task_results": group_results
        }
        all_results[group_name] = final_state

        print(f"  最终坐标系: {cs.get_basis_as_list()}")

    return all_results


# 使用示例
if __name__ == "__main__":

    results = process_json_file('data(1).json')

    with open('processed_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n处理完成！结果已保存到 'processed_results.json'")
