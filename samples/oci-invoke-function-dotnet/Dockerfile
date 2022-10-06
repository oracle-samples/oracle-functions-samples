FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add InvokeFn.csproj
RUN dotnet build InvokeFn.csproj -c Release
RUN dotnet publish InvokeFn.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "InvokeFn.dll"]
CMD ["InvokeFn:Function:function_handler"]